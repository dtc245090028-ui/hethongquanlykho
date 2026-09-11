-- ============================================================
-- seed_data.sql — Dữ liệu mẫu cho hệ thống quản lý kho
-- ============================================================
-- Cách chạy (SQLite):
--   sqlite3 warehouse.db < database/seed_data.sql
--
-- Cách chạy (PostgreSQL):
--   psql -U <user> -d warehouse -f database/seed_data.sql
--
-- Dữ liệu bao gồm:
--   - 6 nhà cung cấp (3 nguyên liệu thô, 2 bán thành phẩm, 1 thành phẩm)
--   - 3 danh mục hàng hóa theo nhóm sản phẩm
--   - 12 hàng hóa, mỗi nhà cung cấp cung cấp 2 hàng hóa
--   - 3 user: 1 admin, 1 warehouse_manager, 1 warehouse_keeper
--
-- MẬT KHẨU MẪU (đã hash bcrypt, password gốc: "Password@123"):
--   Dùng chung cho cả 3 tài khoản để dễ demo
-- ============================================================

-- Xóa dữ liệu cũ theo thứ tự ngược FK để tránh lỗi constraint
DELETE FROM supplier_payments;
DELETE FROM supplier_invoices;
DELETE FROM stocktake_items;
DELETE FROM stocktakes;
DELETE FROM goods_issue_items;
DELETE FROM goods_issues;
DELETE FROM goods_receipt_items;
DELETE FROM goods_receipts;
DELETE FROM purchase_order_items;
DELETE FROM purchase_orders;
DELETE FROM goods;
DELETE FROM categories;
DELETE FROM suppliers;
DELETE FROM users;

-- ============================================================
-- BẢNG: users
-- role: admin | warehouse_manager | warehouse_keeper
-- password_hash: bcrypt hash của "Password@123"
-- (sinh bằng: python -c "import bcrypt; print(bcrypt.hashpw(b'Password@123', bcrypt.gensalt()).decode())")
-- ============================================================
INSERT INTO users (id, username, full_name, email, role, password_hash, is_active, created_at) VALUES
(
    1,
    'admin01',
    'Nguyễn Văn Admin',
    'admin@warehouse.local',
    'admin',
    -- bcrypt hash của "Password@123" (cost=12)
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiJPL9bBjFwMVQ8Ckq3KvWfAZ5Hy',
    1,
    '2026-01-01T08:00:00'
),
(
    2,
    'manager01',
    'Trần Thị Quản Lý',
    'manager@warehouse.local',
    'warehouse_manager',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiJPL9bBjFwMVQ8Ckq3KvWfAZ5Hy',
    1,
    '2026-01-01T08:00:00'
),
(
    3,
    'keeper01',
    'Lê Văn Thủ Kho',
    'keeper@warehouse.local',
    'warehouse_keeper',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiJPL9bBjFwMVQ8Ckq3KvWfAZ5Hy',
    1,
    '2026-01-01T08:00:00'
);

INSERT INTO suppliers (id, name, contact_person, phone, email, address, tax_code, status, notes, created_at, updated_at) VALUES
(
    1,
     'Công ty TNHH Nguyên Liệu Nhựa Việt',
    'Phạm Minh Đức',
    '0901234567',
    'duc.pham@thienlong.vn',
    '123 Đường Lý Thường Kiệt, Q.10, TP.HCM',
    '0312345678',
    'active',
    'Nhà cung cấp nguyên liệu thô: hạt nhựa và phụ gia sản xuất',
    '2026-01-05T09:00:00',
    '2026-01-05T09:00:00'
),
(
    2,
     'Công ty CP Kim Loại Công Nghiệp Đông Nam',
    'Nguyễn Thị Hoa',
    '0912345678',
    'hoa.nt@kimloaidongnam.vn',
    '45 Đường Trần Phú, TX.Thủ Dầu Một, Bình Dương',
    '3702345678',
    'active',
    'Nhà cung cấp nguyên liệu thô: thép cuộn và nhôm tấm',
    '2026-01-10T09:00:00',
    '2026-01-10T09:00:00'
),
(
    3,
     'Công ty TNHH Hóa Chất Sản Xuất Minh Phát',
    'Trần Quốc Hùng',
    '0987654321',
    'hung.tq@minhphatchem.vn',
    '789 Đường Cộng Hòa, Q.Tân Bình, TP.HCM',
    '0312987654',
     'active',
    'Nhà cung cấp nguyên liệu thô: dung môi và hóa chất phụ trợ',
    '2026-02-01T09:00:00',
    '2026-02-01T09:00:00'
),
(
    4, 'Công ty TNHH Linh Kiện Bán Thành Phẩm Á Châu', 'Đỗ Văn Nam',
    '0938123456', 'nam@linhkienachau.vn', '18 Đường Tân Tạo, Q.Bình Tân, TP.HCM',
    '0313456789', 'active', 'Nhà cung cấp bán thành phẩm: cụm mạch và module điều khiển',
    '2026-02-05T09:00:00', '2026-02-05T09:00:00'
),
(
    5, 'Công ty CP Cơ Khí Bán Thành Phẩm Việt Thành', 'Võ Thị Lan',
    '0949234567', 'lan@vietthanhco.vn', '66 Đường Nguyễn Văn Linh, Q.7, TP.HCM',
    '0314567890', 'active', 'Nhà cung cấp bán thành phẩm: khung và vỏ cơ khí gia công sẵn',
    '2026-02-10T09:00:00', '2026-02-10T09:00:00'
),
(
    6, 'Công ty TNHH Sản Phẩm Hoàn Thiện Thành Công', 'Nguyễn Quốc Bảo',
    '0958345678', 'bao@thanhcong.vn', '25 Đường Võ Văn Kiệt, Q.1, TP.HCM',
    '0315678901', 'active', 'Nhà cung cấp thành phẩm: thiết bị hoàn thiện và hàng đóng gói sẵn',
    '2026-02-15T09:00:00', '2026-02-15T09:00:00'
);

-- ============================================================
-- BẢNG: categories — 3 nhóm hàng
-- ============================================================
INSERT INTO categories (id, name) VALUES
(1, 'Nguyên liệu thô'),
(2, 'Bán thành phẩm'),
(3, 'Thành phẩm');

-- ============================================================
-- BẢNG: goods — 8 hàng hóa đa dạng
--
-- Mục đích test cảnh báo Min/Max:
--   SKU001: tồn = 5  | min=20  → DƯỚI MIN   (cần cảnh báo + AI gợi ý nhập)
--   SKU002: tồn = 12 | min=10  → bình thường
--   SKU003: tồn = 3  | min=15  → DƯỚI MIN   (cảnh báo nghiêm trọng)
--   SKU004: tồn = 50 | max=40  → VƯỢT MAX   (tồn dư quá nhiều)
--   SKU005: tồn = 25 | min=20, max=100 → bình thường
--   SKU006: tồn = 8  | min=10  → DƯỚI MIN   (sắp hết)
--   SKU007: tồn = 0  | min=5   → HẾT HÀNG   (cảnh báo khẩn)
--   SKU008: tồn = 200| max=150 → VƯỢT MAX   (dư nhiều)
--
-- Lưu ý: KHÔNG có trường "unit_price" trên goods —
--        giá nhập lưu ở goods_receipt_items.unit_price (ràng buộc nghiệp vụ #2)
-- ============================================================
INSERT INTO goods (id, sku, name, category_id, preferred_supplier_id, unit,
                   min_stock, max_stock, quantity_on_hand,
                   selling_price, description, status, created_at, updated_at) VALUES
(
    1, 'NL001', 'Hạt nhựa PP nguyên sinh',
    1, 1, 'Kg',
    20, 200, 5,
    42000.00,
    'Nguyên liệu thô dùng ép vỏ và chi tiết nhựa',
    'active', '2026-01-15T10:00:00', '2026-01-15T10:00:00'
),
(
    2, 'NL002', 'Phụ gia chống UV cho nhựa',
    1, 1, 'Kg',
    10, 100, 12,
    68000.00,
    'Phụ gia nguyên liệu thô tăng độ bền màu sản phẩm',
    'active', '2026-01-15T10:00:00', '2026-01-15T10:00:00'
),
(
    3, 'NL003', 'Thép cuộn cán nguội',
    1, 2, 'Kg',
    15, 80, 3,
    26500.00,
    'Nguyên liệu thô cho gia công khung và vỏ cơ khí',
    'active', '2026-01-15T10:00:00', '2026-01-15T10:00:00'
),
(
    4, 'NL004', 'Nhôm tấm 2mm',
    1, 2, 'Tấm',
    10, 40, 16,
    185000.00,
    'Nguyên liệu thô dùng gia công mặt dựng thiết bị',
    'active', '2026-01-20T10:00:00', '2026-01-20T10:00:00'
),
(
    5, 'NL005', 'Dung môi công nghiệp IPA',
    1, 3, 'Can',
    20, 100, 25,
    95000.00,
    'Dung môi nguyên liệu thô dùng vệ sinh bề mặt',
    'active', '2026-01-20T10:00:00', '2026-01-20T10:00:00'
),
(
    6, 'NL006', 'Chất đóng rắn epoxy',
    1, 3, 'Kg',
    10, 50, 8,
    145000.00,
    'Hóa chất nguyên liệu thô dùng phối trộn keo epoxy',
    'active', '2026-02-01T10:00:00', '2026-02-01T10:00:00'
),
(
    7, 'BTP001', 'Cụm mạch điều khiển nguồn',
    2, 4, 'Bộ',
    5, 30, 0,
    320000.00,
    'Bán thành phẩm đã lắp linh kiện và kiểm tra chức năng',
    'active', '2026-02-10T10:00:00', '2026-02-10T10:00:00'
),
(
    8, 'BTP002', 'Module hiển thị LCD 16x2',
    2, 4, 'Bộ',
    10, 40, 16,
    98000.00,
    'Bán thành phẩm hiển thị dùng cho thiết bị hoàn chỉnh',
    'active', '2026-02-20T10:00:00', '2026-02-20T10:00:00'
),
(
    9, 'BTP003', 'Khung thép sơn tĩnh điện',
    2, 5, 'Cái', 10, 40, 16, 285000.00,
    'Bán thành phẩm cơ khí đã gia công và sơn hoàn thiện',
    'active', '2026-02-20T10:00:00', '2026-02-20T10:00:00'
),
(
    10, 'BTP004', 'Vỏ nhôm gia công CNC',
    2, 5, 'Cái', 10, 50, 8, 410000.00,
    'Bán thành phẩm vỏ nhôm đã cắt và xử lý bề mặt',
    'active', '2026-02-20T10:00:00', '2026-02-20T10:00:00'
),
(
    11, 'TP001', 'Bộ điều khiển đóng gói hoàn chỉnh',
    3, 6, 'Bộ', 5, 30, 9, 1250000.00,
    'Thành phẩm đã lắp ráp, kiểm thử và đóng gói',
    'active', '2026-02-25T10:00:00', '2026-02-25T10:00:00'
),
(
    12, 'TP002', 'Thiết bị giám sát nhiệt độ',
    3, 6, 'Cái', 5, 25, 4, 890000.00,
    'Thành phẩm sẵn sàng giao cho khách hàng',
    'active', '2026-02-10T10:00:00', '2026-02-10T10:00:00'
);

-- ============================================================
-- BẢNG: purchase_orders / purchase_order_items
-- Dữ liệu mẫu để hiển thị đơn đang xử lý trên Dashboard
-- ============================================================
INSERT INTO purchase_orders (id, supplier_id, created_by, order_date, status, created_at, updated_at) VALUES
(1, 1, 2, '2026-08-27T08:30:00', 'chờ xác nhận', '2026-08-27T08:30:00', '2026-08-27T08:30:00'),
(2, 3, 2, '2026-08-26T14:00:00', 'đang giao',    '2026-08-26T14:00:00', '2026-08-26T14:00:00'),
(3, 1, 2, '2026-08-20T10:00:00', 'đã nhận',      '2026-08-20T10:00:00', '2026-08-22T16:00:00');

INSERT INTO purchase_order_items (po_id, goods_id, quantity_ordered, unit_price) VALUES
(1, 1, 100, 2200),
(1, 2, 30, 68000),
(2, 5, 40, 95000),
(2, 6, 20, 145000),
(3, 2, 100, 1200);

-- ============================================================
-- BẢNG: goods_receipts / goods_receipt_items
-- Có phiếu nhập hôm nay để Dashboard không còn trạng thái trống
-- ============================================================
INSERT INTO goods_receipts (id, supplier_id, po_id, created_by, received_date, note, created_at, updated_at) VALUES
(1, 1, 3, 3, '2026-08-22T15:30:00', 'Đã nhận đủ theo đơn đặt hàng PO-003', '2026-08-22T15:30:00', '2026-08-22T15:30:00'),
(2, 3, 2, 3, '2026-08-27T09:00:00', 'Nhận đợt 1, còn thiếu một phần hóa chất', '2026-08-27T09:00:00', '2026-08-27T09:00:00'),
(3, 1, NULL, 3, '2026-08-27T11:15:00', 'Nhập bổ sung hàng mẫu từ nhà cung cấp', '2026-08-27T11:15:00', '2026-08-27T11:15:00');

INSERT INTO goods_receipt_items (receipt_id, goods_id, quantity, unit_price) VALUES
(1, 2, 100, 1200),
(2, 5, 25, 95000),
(2, 6, 10, 145000),
(3, 1, 20, 2200);

-- ============================================================
-- BẢNG: goods_issues / goods_issue_items
-- Có phiếu xuất hôm nay và một phiếu xuất lịch sử
-- ============================================================
INSERT INTO goods_issues (id, created_by, issued_date, note, created_at, updated_at) VALUES
(1, 3, '2026-08-27T10:00:00', 'Xuất văn phòng phẩm cho phòng hành chính', '2026-08-27T10:00:00', '2026-08-27T10:00:00'),
(2, 3, '2026-08-27T14:20:00', 'Xuất linh kiện cho bộ phận kỹ thuật', '2026-08-27T14:20:00', '2026-08-27T14:20:00'),
(3, 3, '2026-08-25T09:45:00', 'Xuất vật tư cho đơn hàng sản xuất SP-026', '2026-08-25T09:45:00', '2026-08-25T09:45:00');

INSERT INTO goods_issue_items (issue_id, goods_id, quantity) VALUES
(1, 5, 5),
(1, 4, 2),
(2, 2, 3),
(2, 1, 1),
(3, 3, 1);

-- ============================================================
-- BẢNG: stocktakes / stocktake_items
-- ============================================================
INSERT INTO stocktakes (id, created_by, approved_by, stocktake_date, status, note, created_at, updated_at) VALUES
(1, 3, 2, '2026-08-18T09:00:00', 'đã phê duyệt', 'Kiểm kê định kỳ tháng 8', '2026-08-18T09:00:00', '2026-08-19T16:00:00'),
(2, 3, NULL, '2026-08-27T08:00:00', 'chờ phê duyệt', 'Kiểm kê nhanh khu vực linh kiện', '2026-08-27T08:00:00', '2026-08-27T08:00:00');

INSERT INTO stocktake_items (stocktake_id, goods_id, system_quantity, actual_quantity, difference, action) VALUES
(1, 5, 25, 25, 0, 'Không có chênh lệch'),
(1, 4, 50, 48, -2, 'Đã cập nhật hao hụt'),
(2, 1, 5, 4, -1, 'Tìm nguyên nhân thiếu hàng'),
(2, 3, 3, 3, 0, 'Không có chênh lệch');

-- ============================================================
-- BẢNG: supplier_invoices / supplier_payments
-- ============================================================
INSERT INTO supplier_invoices (id, supplier_id, receipt_id, invoice_number, issue_date, total_amount, payment_status, created_at, updated_at) VALUES
(1, 1, 1, 'INV-TL-0822', '2026-08-22T00:00:00', 120000, 'đã thanh toán', '2026-08-22T00:00:00', '2026-08-23T00:00:00'),
(2, 3, 2, 'INV-MP-0827', '2026-08-27T00:00:00', 3550000, 'thanh toán một phần', '2026-08-27T09:00:00', '2026-08-27T09:00:00');

INSERT INTO supplier_payments (invoice_id, amount, payment_date, method) VALUES
(1, 120000, '2026-08-23T00:00:00', 'chuyển khoản'),
(2, 1500000, '2026-08-27T12:00:00', 'chuyển khoản');

-- ============================================================
-- 10 bộ giao dịch lịch sử bổ sung (2025 và tháng 1-7/2026)
-- ============================================================
INSERT INTO purchase_orders (id, supplier_id, created_by, order_date, status, created_at, updated_at) VALUES
(4, 1, 2, '2025-01-14T09:00:00', 'đã nhận', '2025-01-14T09:00:00', '2025-01-16T10:00:00'),
(5, 2, 2, '2025-04-22T10:30:00', 'đang giao', '2025-04-22T10:30:00', '2025-04-23T09:00:00'),
(6, 1, 2, '2025-07-09T14:00:00', 'đã xác nhận', '2025-07-09T14:00:00', '2025-07-10T08:00:00'),
(7, 2, 2, '2025-10-18T08:45:00', 'hủy', '2025-10-18T08:45:00', '2025-10-19T11:00:00'),
(8, 1, 2, '2025-12-05T15:15:00', 'đã nhận', '2025-12-05T15:15:00', '2025-12-07T16:00:00'),
(9, 2, 2, '2026-01-20T09:30:00', 'đã nhận', '2026-01-20T09:30:00', '2026-01-22T14:00:00'),
(10, 1, 2, '2026-02-17T11:00:00', 'đang giao', '2026-02-17T11:00:00', '2026-02-18T09:30:00'),
(11, 2, 2, '2026-03-28T13:45:00', 'đã xác nhận', '2026-03-28T13:45:00', '2026-03-29T10:00:00'),
(12, 1, 2, '2026-05-12T10:15:00', 'hủy', '2026-05-12T10:15:00', '2026-05-13T15:00:00'),
(13, 2, 2, '2026-07-24T16:00:00', 'đã nhận', '2026-07-24T16:00:00', '2026-07-26T09:00:00');

INSERT INTO purchase_order_items (po_id, goods_id, quantity_ordered, unit_price) VALUES
(4, 2, 25, 1500), (5, 3, 30, 2000), (6, 4, 35, 2500), (7, 5, 40, 3000),
(8, 6, 45, 3500), (9, 7, 50, 4000), (10, 8, 55, 4500), (11, 1, 60, 5000),
(12, 2, 65, 5500), (13, 3, 70, 6000);

INSERT INTO goods_receipts (id, supplier_id, po_id, created_by, received_date, note, created_at, updated_at) VALUES
(4, 1, 4, 3, '2025-01-14T09:00:00', 'Nhập hàng đợt 01 theo PO-004', '2025-01-14T09:00:00', '2025-01-14T09:00:00'),
(5, 2, 5, 3, '2025-04-22T10:30:00', 'Nhập hàng đợt 02 theo PO-005', '2025-04-22T10:30:00', '2025-04-22T10:30:00'),
(6, 1, 6, 3, '2025-07-09T14:00:00', 'Nhập hàng đợt 03 theo PO-006', '2025-07-09T14:00:00', '2025-07-09T14:00:00'),
(7, 2, 7, 3, '2025-10-18T08:45:00', 'Nhập hàng đợt 04 theo PO-007', '2025-10-18T08:45:00', '2025-10-18T08:45:00'),
(8, 1, 8, 3, '2025-12-05T15:15:00', 'Nhập hàng đợt 05 theo PO-008', '2025-12-05T15:15:00', '2025-12-05T15:15:00'),
(9, 2, 9, 3, '2026-01-20T09:30:00', 'Nhập hàng đợt 06 theo PO-009', '2026-01-20T09:30:00', '2026-01-20T09:30:00'),
(10, 1, 10, 3, '2026-02-17T11:00:00', 'Nhập hàng đợt 07 theo PO-010', '2026-02-17T11:00:00', '2026-02-17T11:00:00'),
(11, 2, 11, 3, '2026-03-28T13:45:00', 'Nhập hàng đợt 08 theo PO-011', '2026-03-28T13:45:00', '2026-03-28T13:45:00'),
(12, 1, 12, 3, '2026-05-12T10:15:00', 'Nhập hàng đợt 09 theo PO-012', '2026-05-12T10:15:00', '2026-05-12T10:15:00'),
(13, 2, 13, 3, '2026-07-24T16:00:00', 'Nhập hàng đợt 10 theo PO-013', '2026-07-24T16:00:00', '2026-07-24T16:00:00');

INSERT INTO goods_receipt_items (receipt_id, goods_id, quantity, unit_price) VALUES
(4, 2, 16, 1500), (5, 3, 17, 2000), (6, 4, 18, 2500), (7, 5, 19, 3000),
(8, 6, 20, 3500), (9, 7, 21, 4000), (10, 8, 22, 4500), (11, 1, 23, 5000),
(12, 2, 24, 5500), (13, 3, 25, 6000);

INSERT INTO goods_issues (id, created_by, issued_date, note, created_at, updated_at) VALUES
(4, 3, '2025-01-14T09:00:00', 'Xuất hàng cho bộ phận sử dụng đợt 01', '2025-01-14T09:00:00', '2025-01-14T09:00:00'),
(5, 3, '2025-04-22T10:30:00', 'Xuất hàng cho bộ phận sử dụng đợt 02', '2025-04-22T10:30:00', '2025-04-22T10:30:00'),
(6, 3, '2025-07-09T14:00:00', 'Xuất hàng cho bộ phận sử dụng đợt 03', '2025-07-09T14:00:00', '2025-07-09T14:00:00'),
(7, 3, '2025-10-18T08:45:00', 'Xuất hàng cho bộ phận sử dụng đợt 04', '2025-10-18T08:45:00', '2025-10-18T08:45:00'),
(8, 3, '2025-12-05T15:15:00', 'Xuất hàng cho bộ phận sử dụng đợt 05', '2025-12-05T15:15:00', '2025-12-05T15:15:00'),
(9, 3, '2026-01-20T09:30:00', 'Xuất hàng cho bộ phận sử dụng đợt 06', '2026-01-20T09:30:00', '2026-01-20T09:30:00'),
(10, 3, '2026-02-17T11:00:00', 'Xuất hàng cho bộ phận sử dụng đợt 07', '2026-02-17T11:00:00', '2026-02-17T11:00:00'),
(11, 3, '2026-03-28T13:45:00', 'Xuất hàng cho bộ phận sử dụng đợt 08', '2026-03-28T13:45:00', '2026-03-28T13:45:00'),
(12, 3, '2026-05-12T10:15:00', 'Xuất hàng cho bộ phận sử dụng đợt 09', '2026-05-12T10:15:00', '2026-05-12T10:15:00'),
(13, 3, '2026-07-24T16:00:00', 'Xuất hàng cho bộ phận sử dụng đợt 10', '2026-07-24T16:00:00', '2026-07-24T16:00:00');

INSERT INTO goods_issue_items (issue_id, goods_id, quantity) VALUES
(4, 2, 1), (5, 3, 2), (6, 4, 3), (7, 5, 4), (8, 6, 1),
(9, 7, 2), (10, 8, 3), (11, 1, 4), (12, 2, 1), (13, 3, 2);

INSERT INTO stocktakes (id, created_by, approved_by, stocktake_date, status, note, created_at, updated_at) VALUES
(3, 3, 2, '2025-01-14T09:00:00', 'đã phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 01', '2025-01-14T09:00:00', '2025-01-15T10:00:00'),
(4, 3, NULL, '2025-04-22T10:30:00', 'chờ phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 02', '2025-04-22T10:30:00', '2025-04-22T10:30:00'),
(5, 3, 2, '2025-07-09T14:00:00', 'đã phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 03', '2025-07-09T14:00:00', '2025-07-10T10:00:00'),
(6, 3, NULL, '2025-10-18T08:45:00', 'chờ phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 04', '2025-10-18T08:45:00', '2025-10-18T08:45:00'),
(7, 3, 2, '2025-12-05T15:15:00', 'đã phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 05', '2025-12-05T15:15:00', '2025-12-06T10:00:00'),
(8, 3, NULL, '2026-01-20T09:30:00', 'chờ phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 06', '2026-01-20T09:30:00', '2026-01-20T09:30:00'),
(9, 3, 2, '2026-02-17T11:00:00', 'đã phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 07', '2026-02-17T11:00:00', '2026-02-18T10:00:00'),
(10, 3, NULL, '2026-03-28T13:45:00', 'chờ phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 08', '2026-03-28T13:45:00', '2026-03-28T13:45:00'),
(11, 3, 2, '2026-05-12T10:15:00', 'đã phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 09', '2026-05-12T10:15:00', '2026-05-13T10:00:00'),
(12, 3, NULL, '2026-07-24T16:00:00', 'chờ phê duyệt', 'Kiểm kê khu vực hàng hóa đợt 10', '2026-07-24T16:00:00', '2026-07-24T16:00:00');

INSERT INTO stocktake_items (stocktake_id, goods_id, system_quantity, actual_quantity, difference, action) VALUES
(3, 2, 21, 22, 1, 'Đã cập nhật chênh lệch'), (4, 3, 22, 22, 0, 'Không có chênh lệch'),
(5, 4, 23, 22, -1, 'Đã cập nhật chênh lệch'), (6, 5, 24, 24, 0, 'Không có chênh lệch'),
(7, 6, 25, 26, 1, 'Đã cập nhật chênh lệch'), (8, 7, 26, 26, 0, 'Không có chênh lệch'),
(9, 8, 27, 26, -1, 'Đã cập nhật chênh lệch'), (10, 1, 28, 28, 0, 'Không có chênh lệch'),
(11, 2, 29, 30, 1, 'Đã cập nhật chênh lệch'), (12, 3, 30, 30, 0, 'Không có chênh lệch');

INSERT INTO supplier_invoices (id, supplier_id, receipt_id, invoice_number, issue_date, total_amount, payment_status, created_at, updated_at) VALUES
(3, 1, 4, 'INV-SEED-003', '2025-01-14T00:00:00', 24000, 'đã thanh toán', '2025-01-14T00:00:00', '2025-01-15T00:00:00'),
(4, 2, 5, 'INV-SEED-004', '2025-04-22T00:00:00', 34000, 'thanh toán một phần', '2025-04-22T00:00:00', '2025-04-22T00:00:00'),
(5, 1, 6, 'INV-SEED-005', '2025-07-09T00:00:00', 45000, 'thanh toán một phần', '2025-07-09T00:00:00', '2025-07-09T00:00:00'),
(6, 2, 7, 'INV-SEED-006', '2025-10-18T00:00:00', 57000, 'đã thanh toán', '2025-10-18T00:00:00', '2025-10-19T00:00:00'),
(7, 1, 8, 'INV-SEED-007', '2025-12-05T00:00:00', 70000, 'thanh toán một phần', '2025-12-05T00:00:00', '2025-12-05T00:00:00'),
(8, 2, 9, 'INV-SEED-008', '2026-01-20T00:00:00', 84000, 'thanh toán một phần', '2026-01-20T00:00:00', '2026-01-20T00:00:00'),
(9, 1, 10, 'INV-SEED-009', '2026-02-17T00:00:00', 99000, 'đã thanh toán', '2026-02-17T00:00:00', '2026-02-18T00:00:00'),
(10, 2, 11, 'INV-SEED-010', '2026-03-28T00:00:00', 115000, 'thanh toán một phần', '2026-03-28T00:00:00', '2026-03-28T00:00:00'),
(11, 1, 12, 'INV-SEED-011', '2026-05-12T00:00:00', 132000, 'thanh toán một phần', '2026-05-12T00:00:00', '2026-05-12T00:00:00'),
(12, 2, 13, 'INV-SEED-012', '2026-07-24T00:00:00', 150000, 'đã thanh toán', '2026-07-24T00:00:00', '2026-07-25T00:00:00');

INSERT INTO supplier_payments (invoice_id, amount, payment_date, method) VALUES
(3, 24000, '2025-01-15T00:00:00', 'chuyển khoản'), (4, 17000, '2025-04-22T00:00:00', 'tiền mặt'),
(5, 22500, '2025-07-09T00:00:00', 'ủy nhiệm chi'), (6, 57000, '2025-10-19T00:00:00', 'chuyển khoản'),
(7, 35000, '2025-12-05T00:00:00', 'tiền mặt'), (8, 42000, '2026-01-20T00:00:00', 'ủy nhiệm chi'),
(9, 99000, '2026-02-18T00:00:00', 'chuyển khoản'), (10, 57500, '2026-03-28T00:00:00', 'tiền mặt'),
(11, 66000, '2026-05-12T00:00:00', 'ủy nhiệm chi'), (12, 150000, '2026-07-25T00:00:00', 'chuyển khoản');
