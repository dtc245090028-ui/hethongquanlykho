import pytest
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.main import create_app
from app.models.category import Category
from app.models.goods import Goods
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer


@pytest.fixture
def app():
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "supplier-portal-test-secret-key-32",
        "JWT_SECRET_KEY": "supplier-portal-test-secret-key-32",
    })
    with test_app.app_context():
        db.create_all()
        supplier = Supplier(name="NCC Portal", phone="0900000000", status="active")
        other_supplier = Supplier(name="NCC Khac", phone="0911111111", status="active")
        category = Category(name="Thiet bi")
        db.session.add_all([supplier, other_supplier, category])
        db.session.commit()
        db.session.add_all([
            Goods(sku="PORTAL-01", name="Cam bien nhiet", category_id=category.id, preferred_supplier_id=supplier.id, unit="Cai", selling_price=100000, status="active"),
            Goods(sku="PORTAL-02", name="Day tin hieu", category_id=category.id, preferred_supplier_id=other_supplier.id, unit="Cuon", selling_price=50000, status="active"),
        ])
        db.session.commit()
    yield test_app
    with test_app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_supplier_can_login_view_own_catalog_and_submit_new_offer(client, app):
    response = client.get("/api/supplier-portal/suppliers")
    assert response.status_code == 200
    supplier_id = next(
        item["id"] for item in response.json["data"] if item["name"] == "NCC Portal"
    )

    response = client.post("/api/supplier-portal/login", json={
        "supplier_id": supplier_id,
        "phone": "0900000000",
    })
    assert response.status_code == 200
    token = response.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/supplier-portal/catalog", headers=headers)
    assert response.status_code == 200
    assert [item["sku"] for item in response.json["data"]] == ["PORTAL-01"]

    response = client.post("/api/supplier-portal/offers", json={
        "product_name": "Mat hang thu nghiem",
        "unit": "Bo",
        "quantity_available": 25,
        "proposed_price": 250000,
        "price_reason": "Giao gap theo du an",
    }, headers=headers)
    assert response.status_code == 201

    with app.app_context():
        offer = SupplierOffer.query.one()
        assert offer.supplier_id == supplier_id
        assert offer.goods_id is None
        assert offer.quantity_available == 25
        assert offer.proposed_price == 250000


def test_supplier_cannot_offer_another_suppliers_goods(client):
    suppliers = client.get("/api/supplier-portal/suppliers").json["data"]
    supplier_id = next(item["id"] for item in suppliers if item["name"] == "NCC Portal")
    token = client.post("/api/supplier-portal/login", json={
        "supplier_id": supplier_id,
        "phone": "0900000000",
    }).json["access_token"]

    response = client.post("/api/supplier-portal/offers", json={
        "goods_id": 2,
        "quantity_available": 10,
        "proposed_price": 50000,
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json["error_code"] == "INVALID_GOODS"


def test_admin_can_list_supplier_offers(client, app):
    with app.app_context():
        token = create_access_token(
            identity="1",
            additional_claims={"role": "admin"},
        )

    response = client.get(
        "/api/supplier-portal/offers",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json["data"] == []