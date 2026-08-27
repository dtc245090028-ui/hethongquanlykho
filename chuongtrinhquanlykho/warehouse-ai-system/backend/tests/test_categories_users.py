import pytest

from app.extensions import db
from app.main import create_app
from app.models.category import Category
from app.models.user import User


@pytest.fixture
def app():
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-categories-users-key-for-pytest!",
        "JWT_SECRET_KEY": "test-categories-users-key-for-pytest!",
    })
    with test_app.app_context():
        admin = User(username="admin", full_name="Admin", role="admin")
        admin.set_password("Password@123")
        keeper = User(
            username="keeper", full_name="Keeper", role="warehouse_keeper"
        )
        keeper.set_password("Password@123")
        db.session.add_all([admin, keeper, Category(name="Điện tử")])
        db.session.commit()
    yield test_app
    with test_app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def token(client, username):
    response = client.post("/api/auth/login", json={
        "username": username,
        "password": "Password@123",
    })
    return response.get_json()["access_token"]


def auth_headers(client, username):
    return {"Authorization": f"Bearer {token(client, username)}"}


def test_admin_can_create_and_list_categories(client):
    headers = auth_headers(client, "admin")
    created = client.post("/api/categories", headers=headers, json={"name": "Gia dụng"})
    listed = client.get("/api/categories", headers=headers)

    assert created.status_code == 201
    assert created.get_json()["name"] == "Gia dụng"
    assert listed.status_code == 200
    assert len(listed.get_json()["data"]) == 2


def test_keeper_can_read_but_cannot_create_category(client):
    headers = auth_headers(client, "keeper")
    listed = client.get("/api/categories", headers=headers)
    created = client.post("/api/categories", headers=headers, json={"name": "Khác"})

    assert listed.status_code == 200
    assert created.status_code == 403
    assert created.get_json()["error_code"] == "FORBIDDEN"


def test_duplicate_category_is_rejected(client):
    response = client.post(
        "/api/categories",
        headers=auth_headers(client, "admin"),
        json={"name": " điện tử "},
    )

    assert response.status_code == 409
    assert response.get_json()["error_code"] == "CATEGORY_NAME_DUPLICATE"


def test_admin_can_create_and_update_user(client):
    headers = auth_headers(client, "admin")
    created = client.post("/api/users", headers=headers, json={
        "username": "manager",
        "full_name": "Warehouse Manager",
        "password": "Password@123",
        "role": "warehouse_manager",
    })
    user_id = created.get_json()["id"]
    updated = client.put(
        f"/api/users/{user_id}",
        headers=headers,
        json={"is_active": False},
    )

    assert created.status_code == 201
    assert created.get_json()["role"] == "warehouse_manager"
    assert "password_hash" not in created.get_json()
    assert updated.status_code == 200
    assert updated.get_json()["is_active"] is False


def test_non_admin_cannot_manage_users(client):
    response = client.get("/api/users", headers=auth_headers(client, "keeper"))

    assert response.status_code == 403
    assert response.get_json()["error_code"] == "FORBIDDEN"


def test_user_creation_validates_role_and_password(client):
    response = client.post(
        "/api/users",
        headers=auth_headers(client, "admin"),
        json={
            "username": "bad-user",
            "full_name": "Bad User",
            "password": "short",
            "role": "unknown",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error_code"] == "INVALID_ROLE"
