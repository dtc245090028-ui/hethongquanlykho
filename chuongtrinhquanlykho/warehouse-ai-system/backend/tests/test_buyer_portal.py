import pytest

from app.extensions import db
from app.main import create_app
from app.models.category import Category
from app.models.goods import Goods
from app.models.purchase_order import PurchaseOrder
from app.models.supplier import Supplier
from app.models.user import User


@pytest.fixture
def app():
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "buyer-portal-test-secret-key-32",
        "JWT_SECRET_KEY": "buyer-portal-test-secret-key-32",
    })
    with test_app.app_context():
        db.create_all()
        admin = User(username="admin_buyer", full_name="Admin", role="admin", is_active=True)
        admin.set_password("Password@123")
        category = Category(name="Thiết bị")
        supplier = Supplier(name="NCC Buyer Test", phone="0900000000", status="active")
        db.session.add_all([admin, category, supplier])
        db.session.commit()
        db.session.add(Goods(sku="BUYER-01", name="Thiết bị thử", category_id=category.id, unit="Cái", selling_price=100000, status="active"))
        db.session.commit()
    yield test_app
    with test_app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_buyer_request_can_be_confirmed_into_pending_po(client, app):
    response = client.post("/api/buyer-portal/requests", json={
        "buyer_name": "Công ty TNHH Bao Bì Xanh Việt",
        "items": [{"goods_id": 1, "quantity": 12, "unit_price": 95000}],
    })
    assert response.status_code == 201
    request_id = response.json["id"]

    login = client.post("/api/auth/login", json={"username": "admin_buyer", "password": "Password@123"})
    token = login.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/buyer-portal/requests", headers=headers)
    assert response.status_code == 200
    assert response.json["data"][0]["buyer_name"] == "Công ty TNHH Bao Bì Xanh Việt"

    response = client.post("/api/purchase-orders", json={
        "supplier_id": 1,
        "buyer_request_id": request_id,
        "items": [{"goods_id": 1, "quantity_ordered": 12, "unit_price": 95000}],
    }, headers=headers)
    assert response.status_code == 201
    assert response.json["status"] == "chờ xác nhận"

    with app.app_context():
        record = db.session.get(PurchaseOrder, response.json["id"])
        assert record.items[0].quantity_ordered == 12
        assert record.items[0].unit_price == 95000