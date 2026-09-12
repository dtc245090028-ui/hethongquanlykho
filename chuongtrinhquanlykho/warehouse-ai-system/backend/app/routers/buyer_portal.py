from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.auth.decorators import roles_required
from app.extensions import db
from app.models.buyer_request import BuyerRequest, BuyerRequestItem
from app.models.goods import Goods
from app.models.supplier import Supplier

buyer_portal_bp = Blueprint("buyer_portal", __name__, url_prefix="/api/buyer-portal")


@buyer_portal_bp.route("/buyers", methods=["GET"])
def list_buyers():
    buyers = [
        "Công ty TNHH Bao Bì Xanh Việt", "Công ty CP Cơ Khí Đại Thành",
        "Công ty TNHH Thiết Bị Nhiệt Lạnh An Phát", "Công ty CP Điện Tử Minh Quang",
        "Công ty TNHH Nội Thất Kim Loại Việt", "Công ty CP Sơn Và Vật Liệu Phủ Nam Việt",
        "Công ty TNHH Giải Pháp Hiển Thị Sao Việt", "Công ty CP Gia Công Vỏ Thiết Bị Bắc Nam",
        "Công ty TNHH Tự Động Hóa Đông Dương", "Công ty CP Thiết Bị Điều Khiển Thành Công",
    ]
    return jsonify({"data": [{"id": index + 1, "name": name} for index, name in enumerate(buyers)]}), 200


@buyer_portal_bp.route("/catalog", methods=["GET"])
def buyer_catalog():
    goods = Goods.query.filter_by(status="active").order_by(Goods.name.asc()).all()
    return jsonify({"data": [{"id": item.id, "name": item.name, "sku": item.sku, "unit": item.unit, "price": item.selling_price} for item in goods]}), 200


@buyer_portal_bp.route("/requests", methods=["POST"])
def create_buyer_request():
    data = request.get_json(silent=True) or {}
    buyer_name = (data.get("buyer_name") or "").strip()
    items = data.get("items") or []
    if not buyer_name or not items:
        return jsonify({"error_code": "MISSING_FIELDS", "message": "Vui lòng chọn doanh nghiệp và ít nhất một mặt hàng"}), 400

    request_record = BuyerRequest(buyer_name=buyer_name)
    db.session.add(request_record)
    for item in items:
        goods = db.session.get(Goods, item.get("goods_id"))
        quantity = item.get("quantity")
        unit_price = item.get("unit_price")
        if not goods or goods.status != "active" or quantity is None or float(quantity) <= 0 or unit_price is None or float(unit_price) < 0:
            db.session.rollback()
            return jsonify({"error_code": "INVALID_ITEM", "message": "Mặt hàng, số lượng hoặc đơn giá không hợp lệ"}), 400
        db.session.add(BuyerRequestItem(request=request_record, goods_id=goods.id, quantity=float(quantity), unit_price=float(unit_price)))
    db.session.commit()
    return jsonify(request_record.to_dict(include_items=True)), 201


@buyer_portal_bp.route("/requests", methods=["GET"])
@jwt_required()
@roles_required("admin", "warehouse_keeper", "warehouse_manager")
def list_buyer_requests():
    requests = BuyerRequest.query.order_by(BuyerRequest.created_at.desc()).all()
    return jsonify({"data": [record.to_dict(include_items=True) for record in requests]}), 200


@buyer_portal_bp.route("/requests/<int:request_id>/confirm", methods=["POST"])
@jwt_required()
@roles_required("admin", "warehouse_keeper")
def confirm_buyer_request(request_id):
    record = db.session.get(BuyerRequest, request_id)
    if not record:
        return jsonify({"error_code": "REQUEST_NOT_FOUND", "message": "Không tìm thấy yêu cầu đặt mua"}), 404
    if record.status != "chờ xử lý":
        return jsonify({"error_code": "INVALID_STATUS", "message": "Yêu cầu này đã được xử lý"}), 400
    data = request.get_json(silent=True) or {}
    supplier_id = data.get("supplier_id")
    supplier = db.session.get(Supplier, supplier_id) if supplier_id else None
    if not supplier or supplier.status != "active":
        return jsonify({"error_code": "INVALID_SUPPLIER", "message": "Vui lòng chọn nhà cung cấp đang hoạt động"}), 400

    return jsonify({
        "request": record.to_dict(include_items=True),
        "supplier": {"id": supplier.id, "name": supplier.name},
        "message": "Yêu cầu đã được kiểm tra. Hoàn tất việc tạo đơn trong form đơn đặt hàng.",
    }), 200