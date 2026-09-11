"""
routers/goods_issues.py — Endpoint Phiếu xuất kho
====================================================
Triển khai 3 endpoint theo api_contract.md mục 6:

  GET    /api/goods-issues          Danh sách, filter ngày (phân trang)
  POST   /api/goods-issues          Lập phiếu xuất (transaction, chặn xuất vượt tồn)
  GET    /api/goods-issues/{id}     Chi tiết phiếu xuất

Role cho phép:
    - GET (danh sách + chi tiết): admin, warehouse_keeper, warehouse_manager
    - POST (lập phiếu):           admin, warehouse_keeper

Ràng buộc nghiệp vụ cốt lõi (Prompt.md mục 3.3, 10):
  1. quantity > 0 cho mọi dòng items.
  2. quantity ≤ goods.quantity_on_hand → không cho xuất vượt tồn (tồn kho âm).
  3. Cập nhật goods.quantity_on_hand qua DB transaction:
       db.session.flush() để lấy issue.id → thêm items → trừ tồn → commit()
     Nếu bất kỳ bước nào thất bại, rollback toàn bộ (transaction integrity).
  4. Goods phải có status='active'.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

from app.extensions import db
from app.models.goods_issue import GoodsIssue, GoodsIssueItem
from app.models.goods import Goods
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.decorators import roles_required

# Blueprint đặt url_prefix chuẩn theo api_contract.md
goods_issues_bp = Blueprint(
    "goods_issues", __name__, url_prefix="/api/goods-issues"
)


class GoodsIssueError(Exception):
    """Lỗi nghiệp vụ khi lập phiếu xuất kho."""

    def __init__(self, error_code: str, message: str, status_code: int = 400):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.status_code = status_code


def create_goods_issue_transaction(
    user_id: int,
    items_data: list[dict],
    issued_date: datetime,
    note: str | None = None,
    commit: bool = True,
) -> GoodsIssue:
    """Tạo phiếu xuất và trừ tồn trong cùng một transaction.

    Hàm này được dùng cho cả phiếu xuất tạo thủ công và phiếu xuất tự động
    khi đơn đặt hàng chuyển sang trạng thái ``đã nhận``.
    """
    if not items_data:
        raise GoodsIssueError(
            "MISSING_FIELDS",
            "Phiếu xuất phải có ít nhất 1 dòng hàng hóa (items)",
        )

    goods_map: dict[int, Goods] = {}
    normalized_items: list[tuple[int, float]] = []
    quantity_total_per_goods: dict[int, float] = {}

    for idx, item in enumerate(items_data, start=1):
        goods_id = item.get("goods_id")
        quantity = item.get("quantity")
        if goods_id is None:
            raise GoodsIssueError("MISSING_FIELDS", f"Dòng {idx}: thiếu goods_id")

        try:
            goods_id = int(goods_id)
            quantity = float(quantity)
        except (TypeError, ValueError):
            raise GoodsIssueError(
                "INVALID_QUANTITY",
                f"Dòng {idx}: số lượng xuất phải lớn hơn 0",
            )

        if quantity <= 0:
            raise GoodsIssueError(
                "INVALID_QUANTITY",
                f"Dòng {idx}: số lượng xuất phải lớn hơn 0",
            )

        if goods_id not in goods_map:
            goods = db.session.get(Goods, goods_id)
            if not goods:
                raise GoodsIssueError(
                    "GOODS_NOT_FOUND",
                    f"Dòng {idx}: không tìm thấy hàng hóa ID {goods_id}",
                    404,
                )
            if goods.status == "inactive":
                raise GoodsIssueError(
                    "GOODS_INACTIVE",
                    f"Dòng {idx}: hàng hóa '{goods.name}' đã ngừng kinh doanh",
                )
            goods_map[goods_id] = goods
            quantity_total_per_goods[goods_id] = 0.0

        normalized_items.append((goods_id, quantity))
        quantity_total_per_goods[goods_id] += quantity

    for goods_id, total_quantity in quantity_total_per_goods.items():
        goods = goods_map[goods_id]
        if total_quantity > goods.quantity_on_hand:
            raise GoodsIssueError(
                "INSUFFICIENT_STOCK",
                (
                    f"Hàng hóa '{goods.name}' (SKU: {goods.sku}): số lượng xuất "
                    f"yêu cầu ({total_quantity} {goods.unit}) vượt quá tồn kho "
                    f"hiện tại ({goods.quantity_on_hand} {goods.unit})"
                ),
            )

    try:
        issue = GoodsIssue(
            created_by=user_id,
            issued_date=issued_date,
            note=note,
        )
        db.session.add(issue)
        db.session.flush()

        for goods_id, quantity in normalized_items:
            db.session.add(GoodsIssueItem(
                issue_id=issue.id,
                goods_id=goods_id,
                quantity=quantity,
            ))
            goods_map[goods_id].quantity_on_hand -= quantity
            if goods_map[goods_id].quantity_on_hand < 0:
                raise GoodsIssueError(
                    "INSUFFICIENT_STOCK",
                    f"Tồn kho không đủ cho hàng hóa ID {goods_id}",
                )

        if commit:
            db.session.commit()
        return issue
    except GoodsIssueError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise GoodsIssueError(
            "INTERNAL_SERVER_ERROR",
            "Lỗi khi lưu phiếu xuất. Vui lòng thử lại.",
            500,
        )


# ---------------------------------------------------------------------------
# GET /api/goods-issues — Danh sách phiếu xuất (phân trang, filter)
# ---------------------------------------------------------------------------
@goods_issues_bp.route("", methods=["GET"])
@jwt_required()
@roles_required("admin", "warehouse_keeper", "warehouse_manager")
def get_goods_issues():
    """
    Lấy danh sách phiếu xuất với phân trang và filter tùy chọn.

    Query params:
      page        : Trang hiện tại (mặc định 1)
      page_size   : Số bản ghi mỗi trang (mặc định 20)
      date_from   : Lọc từ ngày (ISO 8601, ví dụ: 2026-08-01)
      date_to     : Lọc đến ngày (ISO 8601)

    Response 200 (phân trang — cấu trúc chuẩn api_contract.md):
      { "total": int, "page": int, "page_size": int, "data": [...] }
    Lưu ý: mảng items KHÔNG trả trong danh sách — gọi GET/{id} để lấy chi tiết.
    """
    # ---- Tham số phân trang ----
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)

    # ---- Tham số filter ----
    date_from_str = request.args.get("date_from")
    date_to_str = request.args.get("date_to")

    # Bắt đầu query tất cả phiếu xuất
    query = GoodsIssue.query

    # Lọc theo khoảng ngày xuất hàng
    if date_from_str:
        try:
            date_from = datetime.fromisoformat(date_from_str)
            query = query.filter(GoodsIssue.issued_date >= date_from)
        except ValueError:
            return jsonify({
                "error_code": "INVALID_DATE_FORMAT",
                "message": "date_from phải theo định dạng ISO 8601 (ví dụ: 2026-08-01)"
            }), 400

    if date_to_str:
        try:
            date_to = datetime.fromisoformat(date_to_str)
            query = query.filter(GoodsIssue.issued_date <= date_to)
        except ValueError:
            return jsonify({
                "error_code": "INVALID_DATE_FORMAT",
                "message": "date_to phải theo định dạng ISO 8601 (ví dụ: 2026-08-31)"
            }), 400

    # Sắp xếp mới nhất trước, phân trang
    pagination = query.order_by(GoodsIssue.issued_date.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )

    return jsonify({
        "total": pagination.total,
        "page": pagination.page,
        "page_size": pagination.per_page,
        # include_items=False → không trả mảng items trong danh sách
        "data": [issue.to_dict() for issue in pagination.items],
    }), 200


# ---------------------------------------------------------------------------
# POST /api/goods-issues — Lập phiếu xuất kho (transaction)
# ---------------------------------------------------------------------------
@goods_issues_bp.route("", methods=["POST"])
@jwt_required()
@roles_required("admin", "warehouse_keeper")
def create_goods_issue():
    """
    Lập phiếu xuất kho — trừ tồn kho theo transaction.

    Request body:
      {
        "issued_date":  string ISO 8601 (tùy chọn, mặc định now),
        "note":         string (tùy chọn),
        "items": [
          {
            "goods_id":  int   (bắt buộc),
            "quantity":  float (bắt buộc, > 0)
          },
          ...
        ]
      }

    Ràng buộc (Prompt.md mục 3.3, 10):
      - items không được rỗng
      - quantity > 0 mỗi dòng
      - quantity ≤ goods.quantity_on_hand → chặn xuất vượt tồn
        (tồn kho KHÔNG được âm — Prompt.md mục 6.2)
      - goods phải active
      - Cập nhật goods.quantity_on_hand qua transaction an toàn

    Response 201: chi tiết phiếu xuất vừa tạo (kèm items)
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "error_code": "INVALID_JSON",
            "message": "Body request không phải JSON hợp lệ"
        }), 400

    issued_date = datetime.now(timezone.utc).replace(tzinfo=None)
    issued_date_str = data.get("issued_date")
    if issued_date_str:
        try:
            issued_date = datetime.fromisoformat(
                issued_date_str.replace("Z", "+00:00")
            ).replace(tzinfo=None)
        except ValueError:
            return jsonify({
                "error_code": "INVALID_DATE_FORMAT",
                "message": "issued_date phải theo chuẩn ISO 8601 (ví dụ: 2026-08-14T08:00:00Z)"
            }), 400

    try:
        issue = create_goods_issue_transaction(
            user_id=int(get_jwt_identity()),
            items_data=data.get("items", []),
            issued_date=issued_date,
            note=data.get("note"),
        )
    except GoodsIssueError as error:
        return jsonify({
            "error_code": error.error_code,
            "message": error.message,
        }), error.status_code

    return jsonify(issue.to_dict(include_items=True)), 201


# ---------------------------------------------------------------------------
# GET /api/goods-issues/<id> — Chi tiết phiếu xuất
# ---------------------------------------------------------------------------
@goods_issues_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@roles_required("admin", "warehouse_keeper", "warehouse_manager")
def get_goods_issue_detail(id):
    """
    Lấy chi tiết phiếu xuất theo ID, bao gồm mảng items đầy đủ.

    Response 200: to_dict(include_items=True)
    Response 404: ISSUE_NOT_FOUND nếu không tồn tại
    """
    issue = db.session.get(GoodsIssue, id)
    if not issue:
        return jsonify({
            "error_code": "ISSUE_NOT_FOUND",
            "message": f"Không tìm thấy phiếu xuất ID {id}"
        }), 404

    return jsonify(issue.to_dict(include_items=True)), 200
