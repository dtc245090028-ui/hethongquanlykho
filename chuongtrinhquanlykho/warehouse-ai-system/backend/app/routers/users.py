from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from app.auth.decorators import roles_required
from app.extensions import db
from app.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")
VALID_ROLES = ("admin", "warehouse_manager", "warehouse_keeper")


def _user_payload(data):
    return {
        "username": (data.get("username") or "").strip(),
        "full_name": (data.get("full_name") or "").strip(),
        "email": (data.get("email") or "").strip() or None,
        "role": data.get("role"),
    }


@users_bp.route("", methods=["GET"])
@jwt_required()
@roles_required("admin")
def list_users():
    users = User.query.order_by(User.username.asc()).all()
    return jsonify({"data": [user.to_dict() for user in users]}), 200


@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@roles_required("admin")
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({
            "error_code": "USER_NOT_FOUND",
            "message": "Không tìm thấy người dùng",
        }), 404
    return jsonify(user.to_dict()), 200


@users_bp.route("", methods=["POST"])
@jwt_required()
@roles_required("admin")
def create_user():
    data = request.get_json(silent=True) or {}
    payload = _user_payload(data)
    password = data.get("password") or ""
    if not payload["username"] or not payload["full_name"] or not password or not payload["role"]:
        return jsonify({
            "error_code": "MISSING_FIELDS",
            "message": "username, full_name, password và role là bắt buộc",
        }), 400
    if payload["role"] not in VALID_ROLES:
        return jsonify({
            "error_code": "INVALID_ROLE",
            "message": "Role không hợp lệ",
        }), 400
    if len(password) < 8:
        return jsonify({
            "error_code": "INVALID_PASSWORD",
            "message": "Mật khẩu phải có ít nhất 8 ký tự",
        }), 400
    if User.query.filter_by(username=payload["username"]).first():
        return jsonify({
            "error_code": "USERNAME_DUPLICATE",
            "message": "Tên đăng nhập đã tồn tại",
        }), 409

    user = User(**payload, is_active=True)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error_code": "USER_DUPLICATE",
            "message": "Thông tin người dùng đã tồn tại",
        }), 409
    return jsonify(user.to_dict()), 201


@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
@roles_required("admin")
def update_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({
            "error_code": "USER_NOT_FOUND",
            "message": "Không tìm thấy người dùng",
        }), 404

    data = request.get_json(silent=True) or {}
    if "full_name" in data:
        full_name = (data.get("full_name") or "").strip()
        if not full_name:
            return jsonify({
                "error_code": "MISSING_FIELDS",
                "message": "full_name không được để trống",
            }), 400
        user.full_name = full_name
    if "email" in data:
        user.email = (data.get("email") or "").strip() or None
    if "role" in data:
        if data["role"] not in VALID_ROLES:
            return jsonify({
                "error_code": "INVALID_ROLE",
                "message": "Role không hợp lệ",
            }), 400
        user.role = data["role"]
    if "is_active" in data:
        user.is_active = bool(data["is_active"])
    if data.get("password"):
        if len(data["password"]) < 8:
            return jsonify({
                "error_code": "INVALID_PASSWORD",
                "message": "Mật khẩu phải có ít nhất 8 ký tự",
            }), 400
        user.set_password(data["password"])

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "error_code": "USER_DUPLICATE",
            "message": "Email đã được sử dụng",
        }), 409
    return jsonify(user.to_dict()), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@roles_required("admin")
def deactivate_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({
            "error_code": "USER_NOT_FOUND",
            "message": "Không tìm thấy người dùng",
        }), 404
    user.is_active = False
    db.session.commit()
    return jsonify({"message": "Đã khóa tài khoản", "user": user.to_dict()}), 200
