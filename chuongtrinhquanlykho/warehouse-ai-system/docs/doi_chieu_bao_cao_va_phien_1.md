# Kết quả đối chiếu: Báo cáo thiếu sót vs. Code thực tế

## ✅ Những điều báo cáo nêu — ĐÚNG

| # | Vấn đề được nêu | Kiểm chứng thực tế |
|---|---|---|
| 1 | Chưa có API CRUD user, khóa/mở tài khoản, đổi role | Có `models/user.py` nhưng không có router `users` nào được đăng ký trong `main.py` |
| 2 | Chưa có audit log nghiệp vụ | Grep toàn bộ backend → không có bảng/model `AuditLog` nào, chỉ có `ai_interaction_log` |
| 3 | Chưa có script backup/restore | Thư mục `scripts/` chỉ có `generate_seed_hash.py` và `seed_docker.sh` |
| 4 | Scheduler chỉ gọi AI và ghi log, không gửi thông báo | Xem `scheduler.py` — chỉ log vào `ai_interaction_logs`, không có email/notification |
| 5 | Chưa có quy trình thanh lý hàng hỏng/hết hạn riêng | `stocktakes.py` có trường `action` nhưng không có API `/liquidate` hay luồng phê duyệt thanh lý |
| 6 | Không có endpoint CRUD danh mục (categories) | Grep routers → không tìm thấy bất kỳ endpoint `/categories` nào |
| 7 | Chưa xử lý đầy đủ số lượng đặt PO vs. thực nhận | `goods_receipts.py` chỉ kiểm tra PO thuộc đúng supplier, không so sánh `quantity_ordered` vs thực nhận |
| 8 | Schemas gần như rỗng | `__init__.py` — chỉ có 4 dòng comment, không có schema nào |
| 9 | AI chỉ gọi Gemini dù có `AI_PROVIDER` | `inventory_report_service.py` hardcode `_call_gemini_api()`; `AI_PROVIDER` chỉ trong `.env.example` |
| 10 | AI báo cáo tồn kho chỉ gửi dữ liệu từ goods | `ai_features.py:21-31` chỉ query `Goods`, không tổng hợp lịch sử nhập/xuất |
| 11 | CORS mở toàn bộ origin | `main.py:66` — `CORS(app, origins="*")` ✓ |
| 12 | Secret mặc định không an toàn | `main.py:110` — `"change_me_in_production"` ✓ |
| 13 | Thiếu marshmallow-sqlalchemy | `requirements.txt` không có `marshmallow-sqlalchemy` ✓ |
| 14 | Có nhiều file database lẫn lộn | Tìm thấy đúng 4 file `.db` ở 4 vị trí khác nhau ✓ |
| 15 | `Query.get()` deprecated | `stocktakes.py:68` — vẫn dùng `Goods.query.get(goods_id)` ở nhiều chỗ |

## ⚠️ Một điểm báo cáo nêu không hoàn toàn chính xác

Báo cáo nói "API AI trả lỗi 500 kèm nội dung exception thô": Thực tế `ai_features.py:34-35` đã wrap error thành `{"error_code": "AI_SERVICE_ERROR", "message": ...}` — đã có xử lý, không lộ exception thô trực tiếp ra response. Tuy nhiên `str(e)` trong `inventory_report_service.py:64` có thể kèm thông tin nội bộ.

## 📌 Kết luận

Báo cáo đúng về cơ bản (~95%). Hầu hết các thiếu sót đều được xác nhận bằng code thực tế. Đây là một bản rà soát trung thực và khá toàn diện.

---

# Đề xuất chia nhỏ việc làm theo phiên

Tổng cộng 5 phiên theo mức độ ưu tiên và phụ thuộc:

## Phiên 1 — Hạ tầng cốt lõi & Fix ngay
**Mục tiêu:** Hệ thống chạy được, đăng nhập được, database sạch

- Seed đúng `backend/app/instance/warehouse.db`
- Sửa hết `Query.get()` → `db.session.get()` (deprecated)
- Sửa hết `datetime.utcnow()` → `datetime.now(timezone.utc)` nếu còn
- Thêm `marshmallow-sqlalchemy` vào `requirements.txt`
- Giải quyết 4 file `.db` lẫn lộn (xóa/document rõ)

## Phiên 2 — Quản lý tài khoản & Audit Log
**Mục tiêu:** Admin quản lý được user, hệ thống ghi nhật ký

- Tạo router `/api/users` (CRUD, khóa/mở, đổi role — chỉ Admin)
- Tạo model + bảng `AuditLog` (ghi lại mọi tạo/hủy phiếu, thanh toán, duyệt)
- Móc audit log vào các router hiện có (goods_receipts, goods_issues, stocktakes, supplier_invoices)

## Phiên 3 — Hoàn thiện nghiệp vụ
**Mục tiêu:** Các luồng nghiệp vụ đầy đủ và đúng

- API CRUD danh mục (`/api/categories`)
- Đối chiếu PO: kiểm tra số lượng đặt vs. thực nhận, cảnh báo lệch
- Quy trình thanh lý hàng hỏng/hết hạn (API riêng, workflow đề xuất → phê duyệt)
- Scheduler gửi thông báo (in-app hoặc log cảnh báo riêng, lưu lịch sử cảnh báo tồn kho)

## Phiên 4 — Hoàn thiện AI & Bảo mật
**Mục tiêu:** AI đúng spec, hệ thống an toàn hơn

- AI inventory report tổng hợp lịch sử nhập/xuất (không chỉ query Goods)
- Cơ chế chia nhỏ dữ liệu khi nhiều SKU (tránh vượt token limit)
- Giới hạn CORS theo domain cụ thể (production)
- Hướng dẫn/config JWT secret an toàn

## Phiên 5 — Tài liệu bàn giao
**Mục tiêu:** Đủ tài liệu theo đặc tả

- Viết `phan_tich_thiet_ke.md`
- Vẽ ERD (`erd.mmd` + ảnh)
- Viết `use_case.md`
- Hoàn thiện `test_report.md` (chạy đủ Auth, AI modules)
- Viết `final_report.md`

---

# Nhật ký thực hiện Phiên 1 (nguyên văn transcript, không tóm tắt)

> vậy bắt đầu phiên 1 đi

▾ Thought for 5s
  Let me start with Session 1 tasks:
  1. Seed đúng `backend/app/instance/warehouse.db`
  2. Sửa hết `Query.get()` → `db.session.get()` (deprecated)
  3. Sửa hết `datetime.utcnow()` → `datetime.now(timezone.utc)` nếu còn
  4. Thêm `marshmallow-sqlalchemy` vào `requirements.txt`
  5. Giải quyết 4 file `.db` lẫn lộn (xóa/document rõ)

  Let me start by looking at what needs to be done more carefully.
  Bắt đầu phiên 1! Tôi sẽ làm song song các việc có thể:

● Search(Query.get deprecated usages)
● Search(utcnow deprecated usages)
  ⎿  Found 11 results
● Find(Seed data SQL file)
  ⎿  Found 1 matches
● Search(All query.get usages)
  ⎿  Found 22 results
● Read(E:/gemini-thu-nghie...ers/goods_issues.py)
  ⎿  Read 312 lines (ctrl+o to collapse)

  Tôi đã có đủ thông tin. Bây giờ bắt đầu sửa từng file song song:

● Read(E:/gemini-thu-nghiem/chuongtri.../app/routers/goods_receipts.py)
  ⎿  Read 91 lines
● Read(E:/gemini-thu-nghiem/chuongtri.../app/routers/goods_receipts.py)
  ⎿  Read 22 lines
● Read(E:/gemini-thu-nghiem/chuongtri...app/routers/purchase_orders.py)
  ⎿  Read 156 lines
● Read(E:/gemini-thu-nghiem/chuongtri...m/backend/app/routers/goods.py)
  ⎿  Read 141 lines
● Read(E:/gemini-thu-nghiem/chuongtri...p/routers/supplier_invoices.py)
  ⎿  Read 26 lines
● Read(E:/gemini-thu-nghiem/chuongtri...p/routers/supplier_invoices.py)
  ⎿  Read 31 lines
● Read(E:/gemini-thu-nghiem/chuongtri...backend/app/routers/reports.py)
  ⎿  Read 18 lines
● Read(E:/gemini-thu-nghiem/chuongtri...backend/app/routers/reports.py)
  ⎿  Read 16 lines
● Read(E:/gemini-thu-nghiem/chuongtri...backend/app/routers/reports.py)
  ⎿  Read 19 lines
● Read(E:/gemini-thu-nghie.../routers/reports.py)
  ⎿  Read 15 lines (ctrl+o to collapse)

  Tôi đã thu thập đủ thông tin. Bắt đầu sửa tất cả các file:

  1. Sửa goods_issues.py — utcnow + Query.get

● Edit(E:/gemini-thu-nghiem/chuongtri...nd/app/routers/goods_issues.py)
  ⎿  +1 / -1 lines
       21    """
       22
       23    from flask import Blueprint, request, jsonify
       24 -  from datetime import datetime
       24 +  from datetime import datetime, timezone
       25
       26    from app.extensions import db
       27    from app.models.goods_issue import GoodsIssue, GoodsIssueItem
● Edit(E:/gemini-thu-nghiem/chuongtri...nd/app/routers/goods_issues.py)
  ⎿  +1 / -1 lines
      152
      153        # ---- Parse issued_date ----
      154        issued_date_str = data.get("issued_date")
      155 -      issued_date = datetime.utcnow()
      155 +      issued_date =
     datetime.now(timezone.utc).replace(tzinfo=None)
      156        if issued_date_str:
      157            try:
      158                # Hỗ trợ cả "Z" (UTC) và "+HH:MM"
● Edit(E:/gemini-thu-nghiem/chuongtri...nd/app/routers/goods_issues.py)
  ⎿  +1 / -1 lines
      192
      193            # Kiểm tra hàng hóa tồn tại và active
      194            if goods_id not in goods_map:
      195 -              goods = Goods.query.get(goods_id)
      195 +              goods = db.session.get(Goods, goods_id)
      196                if not goods:
      197                    return jsonify({
      198                        "error_code": "GOODS_NOT_FOUND",
● Edit(E:/gemini-thu-nghie...ers/goods_issues.py)
  ⎿  +1 / -1 lines
      301        Response 200: to_dict(include_items=True)
      302        Response 404: ISSUE_NOT_FOUND nếu không tồn tại
      303        """
      304 -      issue = GoodsIssue.query.get(id)
      304 +      issue = db.session.get(GoodsIssue, id)
      305        if not issue:
      306            return jsonify({
      307                "error_code": "ISSUE_NOT_FOUND", (ctrl+o to
     collapse)

  2. Sửa goods_receipts.py

● Edit(E:/gemini-thu-nghiem/chuongtri.../app/routers/goods_receipts.py)
  ⎿  +1 / -1 lines
       23    """
       24
       25    from flask import Blueprint, request, jsonify
       26 -  from datetime import datetime
       26 +  from datetime import datetime, timezone
       27
       28    from app.extensions import db
       29    from app.models.goods_receipt import GoodsReceipt,
     GoodsReceiptItem
● Edit(E:/gemini-thu-nghiem/chuongtri.../app/routers/goods_receipts.py)
  ⎿  +1 / -1 lines
      205
      206        # ---- Parse received_date ----
      207        received_date_str = data.get("received_date")
      208 -      received_date = datetime.utcnow()
      208 +      received_date =
     datetime.now(timezone.utc).replace(tzinfo=None)
      209        if received_date_str:
      210            try:
      211                # Hỗ trợ cả "Z" (UTC) và "+HH:MM"
● Edit(E:/gemini-thu-nghiem/chuongtri.../app/routers/goods_receipts.py)
  ⎿  +1 / -1 lines
      176            }), 400
      177
      178        # ---- Kiểm tra Supplier ----
      179 -      supplier = Supplier.query.get(supplier_id)
      179 +      supplier = db.session.get(Supplier, supplier_id)
      180        if not supplier:
      181            return jsonify({
      182                "error_code": "SUPPLIER_NOT_FOUND",
● Edit(E:/gemini-thu-nghiem/chuongtri.../app/routers/goods_receipts.py)
  ⎿  +1 / -1 lines
      191        # ---- Kiểm tra PO (nếu có po_id) ----
      192        po_id = data.get("po_id")
      193        if po_id is not None:
      194 -          po = PurchaseOrder.query.get(po_id)
      194 +          po = db.session.get(PurchaseOrder, po_id)
      195            if not po:
      196                return jsonify({
      197                    "error_code": "PO_NOT_FOUND",
● Edit(E:/gemini-thu-nghiem/chuongtri.../app/routers/goods_receipts.py)
  ⎿  +1 / -1 lines
      249
      250            # Kiểm tra hàng hóa tồn tại và active
      251            if goods_id not in goods_map:
      252 -              goods = Goods.query.get(goods_id)
      252 +              goods = db.session.get(Goods, goods_id)
      253                if not goods:
      254                    return jsonify({
      255                        "error_code": "GOODS_NOT_FOUND",
● Edit(E:/gemini-thu-nghie...s/goods_receipts.py)
  ⎿  +1 / -1 lines
      325        Response 200: to_dict(include_items=True)
      326        Response 404: RECEIPT_NOT_FOUND nếu không tồn tại
      327        """
      328 -      receipt = GoodsReceipt.query.get(id)
      328 +      receipt = db.session.get(GoodsReceipt, id)
      329        if not receipt:
      330            return jsonify({
      331                "error_code": "RECEIPT_NOT_FOUND", (ctrl+o to
     collapse)

  3. Sửa purchase_orders.py

● Edit(E:/gemini-thu-nghiem/chuongtri...app/routers/purchase_orders.py)
  ⎿  +1 / -1 lines
        1    from flask import Blueprint, request, jsonify
        2 -  from datetime import datetime
        2 +  from datetime import datetime, timezone
        3    from typing import Dict, List, Any
        4
        5    from app.extensions import db
● Edit(E:/gemini-thu-nghiem/chuongtri...app/routers/purchase_orders.py)
  ⎿  +1 / -1 lines
       82
       83        # Parse order_date nếu có
       84        order_date_str = data.get("order_date")
       85 -      order_date = datetime.utcnow()
       85 +      order_date =
     datetime.now(timezone.utc).replace(tzinfo=None)
       86        if order_date_str:
       87            try:
       88                # Xử lý chuỗi ISO 8601 (có thể chứa Z)
● Edit(E:/gemini-thu-nghiem/chuongtri...app/routers/purchase_orders.py)
  ⎿  +1 / -1 lines
       63        if not supplier_id or not items_data:
       64            return jsonify({"error_code": "MISSING_FIELDS",
     "message": "Thiếu supplier_id hoặc items"}), 400
       65
       66 -      supplier = Supplier.query.get(supplier_id)
       66 +      supplier = db.session.get(Supplier, supplier_id)
       67        if not supplier or supplier.status == 'inactive':
       68            return jsonify({"error_code": "INVALID_SUPPLIER",
     "message": "Nhà cung cấp không tồn tại hoặc đã ngừng hợp tác"}), 400
       69
● Edit(E:/gemini-thu-nghiem/chuongtri...app/routers/purchase_orders.py)
  ⎿  +1 / -1 lines
       73            if qty is None or float(qty) <= 0:
       74                return jsonify({"error_code": "INVALID_QUANTITY",
     "message": "Số lượng đặt hàng phải lớn hơn 0"}), 400
       75
       76 -          goods = Goods.query.get(item.get("goods_id"))
       76 +          goods = db.session.get(Goods, item.get("goods_id"))
       77            if not goods or goods.status == 'inactive':
       78                return jsonify({"error_code": "INVALID_GOODS",
     "message": f"Hàng hóa ID {item.get('goods_id')} không tồn tại hoặc
     ngừng kinh doanh"}), 400
       79
● Edit(E:/gemini-thu-nghiem/chuongtri...app/routers/purchase_orders.py)
  ⎿  +1 / -1 lines
      117    @roles_required("warehouse_keeper", "warehouse_manager")
      118    def get_purchase_order_details(id):
      119        """Lấy chi tiết PO"""
      120 -      po = PurchaseOrder.query.get(id)
      120 +      po = db.session.get(PurchaseOrder, id)
      121        if not po:
      122            return jsonify({"error_code": "PO_NOT_FOUND",
     "message": "Không tìm thấy Purchase Order"}), 404
      123
● Edit(E:/gemini-thu-nghie.../purchase_orders.py)
  ⎿  +1 / -1 lines
      136        if new_status not in VALID_TRANSITIONS:
      137            return jsonify({"error_code": "INVALID_STATUS",
     "message": "Trạng thái không hợp lệ"}), 400
      138
      139 -      po = PurchaseOrder.query.get(id)
      139 +      po = db.session.get(PurchaseOrder, id)
      140        if not po:
      141            return jsonify({"error_code": "PO_NOT_FOUND",
     "message": "Không tìm thấy Purchase Order"}), 404
      142     (ctrl+o to collapse)

  4. Sửa goods.py

● Edit(E:/gemini-thu-nghie...pp/routers/goods.py)
  ⎿  +1 / -1 lines
       92    @jwt_required()
       93    @roles_required("admin", "warehouse_manager",
     "warehouse_keeper")
       94    def get_goods_detail(goods_id):
       95 -      goods = Goods.query.get(goods_id)
       95 +      goods = db.session.get(Goods, goods_id)
       96        if not goods:
       97            return jsonify({"error_code": "NOT_FOUND", "message":
     "Không tìm thấy hàng hóa"}), 404
       98        return jsonify(goods.to_dict()), 200
● Edit(E:/gemini-thu-nghiem/chuongtrinhquanlykho/warehouse-ai-
system/backend/app/routers/goods.py)
  ⎿  +1 / -1 lines
 101    @jwt_required()
 102    @roles_required("admin", "warehouse_manager")
 103    def update_goods(goods_id):
 104 -      goods = Goods.query.get(goods_id)
 104 +      goods = db.session.get(Goods, goods_id)
 105        if not goods:
 106            return jsonify({"error_code": "NOT_FOUND", "message":
"Không tìm thấy hàng hóa"}), 404
 107     (ctrl+o to collapse)

  5. Sửa stocktakes.py

● Edit(E:/gemini-thu-nghiem/chuongtri...kend/app/routers/stocktakes.py)
  ⎿  +1 / -1 lines
       65                        "message": "Số lượng thực tế không được nhỏ
     hơn 0"
       66                    }), 400
       67
       68 -              goods = Goods.query.get(goods_id)
       68 +              goods = db.session.get(Goods, goods_id)
       69                if not goods:
       70                    db.session.rollback()
       71                    return jsonify({
● Edit(E:/gemini-thu-nghiem/chuongtri...kend/app/routers/stocktakes.py)
  ⎿  +1 / -1 lines
      106    @jwt_required()
      107    @roles_required("warehouse_keeper")
      108    def propose_stocktake(stocktake_id):
      109 -      stocktake = Stocktake.query.get(stocktake_id)
      109 +      stocktake = db.session.get(Stocktake, stocktake_id)
      110        if not stocktake:
      111            return jsonify({
      112                "error_code": "STOCKTAKE_NOT_FOUND",
● Edit(E:/gemini-thu-nghiem/chuongtri...kend/app/routers/stocktakes.py)
  ⎿  +1 / -1 lines
      166    @jwt_required()
      167    @roles_required("admin", "warehouse_manager")
      168    def approve_stocktake(stocktake_id):
      169 -      stocktake = Stocktake.query.get(stocktake_id)
      169 +      stocktake = db.session.get(Stocktake, stocktake_id)
      170        if not stocktake:
      171            return jsonify({
      172                "error_code": "STOCKTAKE_NOT_FOUND",
● Edit(E:/gemini-thu-nghie...uters/stocktakes.py)
  ⎿  +1 / -1 lines
      181
      182        try:
      183            for item in stocktake.items:
      184 -              goods = Goods.query.get(item.goods_id)
      184 +              goods = db.session.get(Goods, item.goods_id)
      185                if goods:
      186                    goods.quantity_on_hand = item.actual_quantity
      187             (ctrl+o to collapse)

  6. Sửa supplier_invoices.py

● Search(Supplier invoices datetime import)
  ⎿  Found 1 results
● Edit(E:/gemini-thu-nghiem/chuongtri...p/routers/supplier_invoices.py)
  ⎿  +1 / -1 lines
       25    """
       26
       27    from flask import Blueprint, request, jsonify
       28 -  from datetime import datetime
       28 +  from datetime import datetime, timezone
       29
       30    from app.extensions import db
       31    from app.models.supplier_invoice import SupplierInvoice,
     SupplierPayment
● Edit(E:/gemini-thu-nghiem/chuongtri...p/routers/supplier_invoices.py)
  ⎿  +1 / -1 lines
      159            }), 404
      160
      161        # ---- Parse issue_date ----
      162 -      issue_date = datetime.utcnow()
      162 +      issue_date =
     datetime.now(timezone.utc).replace(tzinfo=None)
      163        issue_date_str = data.get("issue_date")
      164        if issue_date_str:
      165            try:
● Edit(E:/gemini-thu-nghie...upplier_invoices.py)
  ⎿  +1 / -1 lines
      318            }), 400
      319
      320        # ---- Parse payment_date ----
      321 -      payment_date = datetime.utcnow()
      321 +      payment_date =
     datetime.now(timezone.utc).replace(tzinfo=None)
      322        payment_date_str = data.get("payment_date")
      323        if payment_date_str:
      324            try: (ctrl+o to collapse)

  7. Sửa reports.py — 4 lần utcnow

● Search(Reports datetime import line)
  ⎿  Found 1 results
● Edit(E:/gemini-thu-nghiem/chuongtri...backend/app/routers/reports.py)
  ⎿  +1 / -1 lines
       27
       28    from flask import Blueprint, request, jsonify
       29    from sqlalchemy import func
       30 -  from datetime import datetime
       30 +  from datetime import datetime, timezone
       31
       32    from app.extensions import db
       33    from app.models.goods import Goods
● Edit(E:/gemini-thu-nghie.../routers/reports.py)
  ⎿  +1 / -1 lines
      172            })
      173
      174        return jsonify({
      175 -          "generated_at": datetime.utcnow().isoformat(),
      175 +          "generated_at": datetime.now(timezone.utc).isoformat(),
      176            "filters": {
      177                "date_from": date_from_str,
      178                "date_to": date_to_str,
● Edit(E:/gemini-thu-nghiem/chuongtrinhquanlykho/warehouse-ai-
system/backend/app/routers/reports.py)
  ⎿  +1 / -1 lines
 309        )
 310
 311        return jsonify({
 312 -          "generated_at": datetime.utcnow().isoformat(),
 312 +          "generated_at": datetime.now(timezone.utc).isoformat(),
 313            "filters": {
 314                "date_from": date_from_str,
 315                "date_to": date_to_str,
● Edit(E:/gemini-thu-nghiem/chuongtrinhquanlykho/warehouse-ai-
system/backend/app/routers/reports.py)
  ⎿  +1 / -1 lines
 385            return jsonify({"error_code": "INVALID_DATE_FORMAT",
"message": str(e)}), 400
 386
 387        result = {
 388 -          "generated_at": datetime.utcnow().isoformat(),
 388 +          "generated_at": datetime.now(timezone.utc).isoformat(),
 389            "filters": {
 390                "date_from": date_from_str,
 391                "date_to": date_to_str,
● Edit(E:/gemini-thu-nghiem/chuongtrinhquanlykho/warehouse-ai-
system/backend/app/routers/reports.py)
  ⎿  +1 / -1 lines
 592            })
 593
 594        return jsonify({
 595 -          "generated_at": datetime.utcnow().isoformat(),
 595 +          "generated_at": datetime.now(timezone.utc).isoformat(),
 596            "filters": {
 597                "date_from": date_from_str,
 598                "date_to": date_to_str, (ctrl+o to collapse)
  8. Sửa test files

● Read(E:/gemini-thu-nghiem/chuongtri...ests/test_supplier_invoices.py)
  ⎿  Read 16 lines
● Read(E:/gemini-thu-nghiem/chuongtri...ests/test_supplier_invoices.py)
  ⎿  Read 14 lines
● Search(Test supplier invoices import line)
  ⎿  Found 1 results
● Search(Test goods issues import)
● Edit(E:/gemini-thu-nghie...upplier_invoices.py)
  ⎿  +1 / -1 lines
       10    """
       11
       12    import pytest
       13 -  from datetime import datetime
       13 +  from datetime import datetime, timezone
       14    from app.main import create_app
       15    from app.extensions import db
       16    from app.models.user import User (ctrl+o to collapse)
