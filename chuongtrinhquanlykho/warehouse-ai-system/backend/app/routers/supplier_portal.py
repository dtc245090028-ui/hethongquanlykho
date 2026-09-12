from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required

from app.extensions import db
from app.models.goods import Goods
from app.models.supplier import Supplier
from app.models.supplier_offer import SupplierOffer
from app.auth.decorators import roles_required


supplier_portal_bp = Blueprint("supplier_portal", __name__, url_prefix="/api/supplier-portal")


def supplier_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "supplier" or not claims.get("supplier_id"):
            return jsonify({
                "error_code": "FORBIDDEN",
                "message": "Chỉ nhà cung cấp đã đăng nhập mới được sử dụng chức năng này",
            }), 403
        return fn(*args, **kwargs)
    return wrapper


@supplier_portal_bp.route("/suppliers", methods=["GET"])
def list_login_suppliers():
    suppliers = Supplier.query.filter_by(status="active").order_by(Supplier.name.asc()).all()
    return jsonify({"data": [{"id": supplier.id, "name": supplier.name} for supplier in suppliers]}), 200


@supplier_portal_bp.route("/login", methods=["POST"])
def supplier_login():
    data = request.get_json(silent=True) or {}
    supplier_id = data.get("supplier_id")
    phone = (data.get("phone") or "").strip()
    supplier = db.session.get(Supplier, supplier_id) if supplier_id else None

    if not supplier or supplier.status != "active" or not phone or phone != (supplier.phone or ""):
        return jsonify({
            "error_code": "INVALID_CREDENTIALS",
            "message": "Tên nhà cung cấp hoặc số điện thoại không chính xác",
        }), 401

    access_token = create_access_token(
        identity=f"supplier:{supplier.id}",
        additional_claims={"role": "supplier", "supplier_id": supplier.id},
    )
    return jsonify({
        "access_token": access_token,
        "role": "supplier",
        "supplier": {"id": supplier.id, "name": supplier.name},
    }), 200


@supplier_portal_bp.route("/catalog", methods=["GET"])
@supplier_required
def supplier_catalog():
    supplier_id = get_jwt().get("supplier_id")
    goods = Goods.query.filter_by(preferred_supplier_id=supplier_id, status="active").order_by(Goods.name.asc()).all()
    return jsonify({
        "data": [{
            "id": item.id,
            "sku": item.sku,
            "name": item.name,
            "unit": item.unit,
            "reference_price": item.selling_price,
        } for item in goods]
    }), 200


@supplier_portal_bp.route("/offers", methods=["POST"])
@supplier_required
def create_supplier_offer():
    data = request.get_json(silent=True) or {}
    supplier_id = get_jwt().get("supplier_id")
    goods_id = data.get("goods_id")
    product_name = (data.get("product_name") or "").strip()
    unit = (data.get("unit") or "").strip()
    reason = (data.get("price_reason") or "").strip() or None

    try:
        quantity_available = float(data.get("quantity_available"))
    except (TypeError, ValueError):
        quantity_available = 0
    if quantity_available <= 0:
        return jsonify({
            "error_code": "INVALID_QUANTITY",
            "message": "Số lượng chào bán phải lớn hơn 0",
        }), 400

    if goods_id:
        goods = db.session.get(Goods, goods_id)
        if not goods or goods.status != "active" or goods.preferred_supplier_id != supplier_id:
            return jsonify({
                "error_code": "INVALID_GOODS",
                "message": "Mặt hàng không thuộc danh mục bán của nhà cung cấp này",
            }), 400
        product_name = goods.name
        unit = goods.unit
    elif not product_name or not unit:
        return jsonify({
            "error_code": "MISSING_FIELDS",
            "message": "Mặt hàng mới cần có tên và đơn vị tính",
        }), 400

    try:
        proposed_price = float(data.get("proposed_price"))
    except (TypeError, ValueError):
        proposed_price = -1
    if proposed_price < 0:
        return jsonify({
            "error_code": "INVALID_PRICE",
            "message": "Giá chào bán phải là số không âm",
        }), 400

    offer = SupplierOffer(
        supplier_id=supplier_id,
        goods_id=goods_id or None,
        product_name=product_name,
        unit=unit,
        quantity_available=quantity_available,
        proposed_price=proposed_price,
        price_reason=reason,
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify(offer.to_dict()), 201


@supplier_portal_bp.route("/offers", methods=["GET"])
@jwt_required()
@roles_required("admin", "warehouse_manager")
def list_supplier_offers():
    """Danh sách chào bán để bộ phận kho xem và đưa vào form hàng hóa."""
    offers = SupplierOffer.query.order_by(SupplierOffer.created_at.desc()).all()
    data = []
    for offer in offers:
        item = offer.to_dict()
        item["supplier_name"] = offer.supplier.name
        item["sku"] = offer.goods.sku if offer.goods else None
        item["category_id"] = offer.goods.category_id if offer.goods else None
        data.append(item)
    return jsonify({"data": data}), 200