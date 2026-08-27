from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.auth.decorators import roles_required
from app.extensions import db
from app.models.category import Category

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


def _find_duplicate_name(name, category_id=None):
    normalized_name = name.casefold()
    return next(
        (
            category
            for category in Category.query.all()
            if category.id != category_id
            and category.name.casefold() == normalized_name
        ),
        None,
    )


@categories_bp.route("", methods=["GET"])
@jwt_required()
def list_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({"data": [category.to_dict() for category in categories]}), 200


@categories_bp.route("/<int:category_id>", methods=["GET"])
@jwt_required()
def get_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({
            "error_code": "CATEGORY_NOT_FOUND",
            "message": "Không tìm thấy danh mục",
        }), 404
    return jsonify(category.to_dict()), 200


@categories_bp.route("", methods=["POST"])
@jwt_required()
@roles_required("admin", "warehouse_manager")
def create_category():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({
            "error_code": "MISSING_FIELDS",
            "message": "Tên danh mục là bắt buộc",
        }), 400

    if _find_duplicate_name(name):
        return jsonify({
            "error_code": "CATEGORY_NAME_DUPLICATE",
            "message": "Tên danh mục đã tồn tại",
        }), 409

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@categories_bp.route("/<int:category_id>", methods=["PUT"])
@jwt_required()
@roles_required("admin", "warehouse_manager")
def update_category(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        return jsonify({
            "error_code": "CATEGORY_NOT_FOUND",
            "message": "Không tìm thấy danh mục",
        }), 404

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({
            "error_code": "MISSING_FIELDS",
            "message": "Tên danh mục là bắt buộc",
        }), 400

    duplicate = _find_duplicate_name(name, category_id)
    if duplicate:
        return jsonify({
            "error_code": "CATEGORY_NAME_DUPLICATE",
            "message": "Tên danh mục đã tồn tại",
        }), 409

    category.name = name
    db.session.commit()
    return jsonify(category.to_dict()), 200
