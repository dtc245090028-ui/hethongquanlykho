"""Concurrency tests for inventory updates.

These tests intentionally exercise the current read-check-write handlers without
adding locks or changing application code. They use a file-backed SQLite database
so every worker thread shares the same database state.
"""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from app.extensions import db
from app.main import create_app
from app.models.category import Category
from app.models.goods import Goods
from app.models.supplier import Supplier
from app.models.user import User


WORKER_COUNT = 10
QUANTITY_PER_REQUEST = 15
INITIAL_STOCK = 100


@pytest.fixture
def app(tmp_path):
    """Create one shared file-backed database for all worker threads."""
    database_path = tmp_path / "concurrency.sqlite"
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "connect_args": {"timeout": 30},
        },
        "JWT_EXPIRE_MINUTES": "60",
        "SECRET_KEY": "concurrency-test-secret-key-32-bytes",
        "JWT_SECRET_KEY": "concurrency-test-secret-key-32-bytes",
    })

    with test_app.app_context():
        db.create_all()

        keeper = User(
            username="concurrency_keeper",
            full_name="Concurrency Keeper",
            email="concurrency@test.local",
            role="warehouse_keeper",
            is_active=True,
        )
        keeper.set_password("Password@123")
        category = Category(name="Concurrency Category")
        supplier = Supplier(name="Concurrency Supplier", status="active")
        db.session.add_all([keeper, category, supplier])
        db.session.flush()

        goods = Goods(
            sku="CONCURRENCY-001",
            name="Concurrency Item",
            category_id=category.id,
            unit="Cái",
            min_stock=0,
            quantity_on_hand=INITIAL_STOCK,
            status="active",
        )
        db.session.add(goods)
        db.session.commit()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()


def _login(app):
    with app.test_client() as client:
        response = client.post(
            "/api/auth/login",
            json={
                "username": "concurrency_keeper",
                "password": "Password@123",
            },
        )
    assert response.status_code == 200
    return response.get_json()["access_token"]


def _run_concurrently(app, path, payload, token):
    barrier = Barrier(WORKER_COUNT)

    def send_request(_worker_id):
        with app.test_client() as client:
            barrier.wait()
            try:
                response = client.post(
                    path,
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"},
                )
                return response.status_code, response.get_json(silent=True)
            except Exception as error:  # pragma: no cover - diagnostic path
                return None, {"exception": repr(error)}

    with ThreadPoolExecutor(max_workers=WORKER_COUNT) as executor:
        return list(executor.map(send_request, range(WORKER_COUNT)))


def _stock_quantity(app):
    with app.app_context():
        return db.session.query(Goods.quantity_on_hand).filter_by(
            sku="CONCURRENCY-001"
        ).scalar()


def test_concurrent_goods_issues_do_not_oversell(app):
    """Ten concurrent exports must allow only six requests to succeed."""
    token = _login(app)
    results = _run_concurrently(
        app,
        "/api/goods-issues",
        {"items": [{"goods_id": 1, "quantity": QUANTITY_PER_REQUEST}]},
        token,
    )

    successful_count = sum(status_code == 201 for status_code, _ in results)
    final_quantity = _stock_quantity(app)
    expected_quantity = INITIAL_STOCK - successful_count * QUANTITY_PER_REQUEST

    print(
        "goods-issues concurrency: "
        f"successes={successful_count}, "
        f"final_quantity={final_quantity}, "
        f"expected_quantity={expected_quantity}, "
        f"statuses={[status_code for status_code, _ in results]}"
    )

    assert successful_count == 6, (
        "Concurrent export result is not serialized: "
        f"expected 6 successful requests, got {successful_count}; "
        f"final quantity={final_quantity}"
    )
    assert final_quantity == expected_quantity, (
        "Lost update or partial transaction detected: "
        f"actual final quantity={final_quantity}, "
        f"expected={expected_quantity}"
    )
    assert final_quantity >= 0


def test_concurrent_goods_receipts_do_not_lose_updates(app):
    """Ten concurrent receipts must accumulate all ten quantity updates."""
    token = _login(app)
    results = _run_concurrently(
        app,
        "/api/goods-receipts",
        {
            "supplier_id": 1,
            "items": [{
                "goods_id": 1,
                "quantity": QUANTITY_PER_REQUEST,
                "unit_price": 10,
            }],
        },
        token,
    )

    successful_count = sum(status_code == 201 for status_code, _ in results)
    final_quantity = _stock_quantity(app)
    expected_quantity = INITIAL_STOCK + successful_count * QUANTITY_PER_REQUEST

    print(
        "goods-receipts concurrency: "
        f"successes={successful_count}, "
        f"final_quantity={final_quantity}, "
        f"expected_quantity={expected_quantity}, "
        f"statuses={[status_code for status_code, _ in results]}"
    )

    assert successful_count == WORKER_COUNT, (
        "Concurrent receipt requests were not all successful: "
        f"expected {WORKER_COUNT}, got {successful_count}; "
        f"final quantity={final_quantity}"
    )
    assert final_quantity == expected_quantity, (
        "Lost update detected: "
        f"actual final quantity={final_quantity}, "
        f"expected={expected_quantity}"
    )