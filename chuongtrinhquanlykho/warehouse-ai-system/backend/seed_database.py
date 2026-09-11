#!/usr/bin/env python
"""
seed_database.py — Khởi tạo database với seed data
Chạy: python seed_database.py
"""
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import create_app
from app.extensions import db
from app.models import (
    User, Supplier, Category, Goods, PurchaseOrder, PurchaseOrderItem,
    GoodsReceipt, GoodsReceiptItem, GoodsIssue, GoodsIssueItem,
    Stocktake, StocktakeItem, SupplierInvoice, SupplierPayment, AIInteractionLog
)

def seed_database():
    """Create tables and insert seed data"""
    app = create_app()
    
    with app.app_context():
        # Step 1: Create all tables
        print("1️⃣  Creating tables...")
        db.create_all()
        print("   ✅ Tables created")
        
        # Step 2: Clear existing data
        print("2️⃣  Clearing existing data...")
        db.session.query(SupplierPayment).delete()
        db.session.query(SupplierInvoice).delete()
        db.session.query(StocktakeItem).delete()
        db.session.query(Stocktake).delete()
        db.session.query(GoodsIssueItem).delete()
        db.session.query(GoodsIssue).delete()
        db.session.query(GoodsReceiptItem).delete()
        db.session.query(GoodsReceipt).delete()
        db.session.query(PurchaseOrderItem).delete()
        db.session.query(PurchaseOrder).delete()
        db.session.query(User).delete()
        db.session.query(Supplier).delete()
        db.session.query(Category).delete()
        db.session.query(Goods).delete()
        db.session.commit()
        print("   ✅ Existing data cleared")
        
        # Step 3: Insert users
        print("3️⃣  Inserting users...")
        # Password hash for "Password@123" (bcrypt rounds=12)
        password_hash = '$2b$12$qycgHYuKiLRPt4Pu6e8M8u.w6BgUIpiStyyNHHhpRzQxdXho04qNy'
        users = [
            User(
                id=1,
                username='admin01',
                full_name='Nguyễn Văn Admin',
                email='admin@warehouse.local',
                role='admin',
                password_hash=password_hash,
                is_active=True,
            ),
            User(
                id=2,
                username='manager01',
                full_name='Trần Thị Quản Lý',
                email='manager@warehouse.local',
                role='warehouse_manager',
                password_hash=password_hash,
                is_active=True,
            ),
            User(
                id=3,
                username='keeper01',
                full_name='Lê Văn Thủ Kho',
                email='keeper@warehouse.local',
                role='warehouse_keeper',
                password_hash=password_hash,
                is_active=True,
            ),
        ]
        db.session.add_all(users)
        db.session.commit()
        print("   ✅ 3 users created")
        for u in users:
            print(f"      - {u.username} ({u.role})")
        
        # Step 4: Insert suppliers
        print("3️⃣  Inserting suppliers...")
        suppliers = [
            Supplier(
                id=1,
                name='Công ty TNHH Nguyên Liệu Nhựa Việt',
                contact_person='Phạm Minh Đức',
                phone='0901234567',
                email='duc.pham@nguyenlieunhua.vn',
                address='123 Đường Lý Thường Kiệt, Q.10, TP.HCM',
                tax_code='0312345678',
                status='active',
                notes='Nhà cung cấp nguyên liệu thô: hạt nhựa và phụ gia sản xuất',
            ),
            Supplier(
                id=2,
                name='Công ty CP Kim Loại Công Nghiệp Đông Nam',
                contact_person='Nguyễn Thị Hoa',
                phone='0912345678',
                email='hoa.nt@kimloaidongnam.vn',
                address='45 Đường Trần Phú, TX.Thủ Dầu Một, Bình Dương',
                tax_code='3702345678',
                status='active',
                notes='Nhà cung cấp nguyên liệu thô: thép cuộn và nhôm tấm',
            ),
            Supplier(
                id=3,
                name='Công ty TNHH Hóa Chất Sản Xuất Minh Phát',
                contact_person='Trần Quốc Hùng',
                phone='0987654321',
                email='hung.tq@minhphatchem.vn',
                address='789 Đường Cộng Hòa, Q.Tân Bình, TP.HCM',
                tax_code='0312987654',
                status='active',
                notes='Nhà cung cấp nguyên liệu thô: dung môi và hóa chất phụ trợ',
            ),
            Supplier(
                id=4,
                name='Công ty TNHH Linh Kiện Bán Thành Phẩm Á Châu',
                contact_person='Đỗ Văn Nam', phone='0938123456',
                email='nam@linhkienachau.vn',
                address='18 Đường Tân Tạo, Q.Bình Tân, TP.HCM', tax_code='0313456789',
                status='active',
                notes='Nhà cung cấp bán thành phẩm: cụm mạch và module điều khiển',
            ),
            Supplier(
                id=5,
                name='Công ty CP Cơ Khí Bán Thành Phẩm Việt Thành',
                contact_person='Võ Thị Lan', phone='0949234567',
                email='lan@vietthanhco.vn',
                address='66 Đường Nguyễn Văn Linh, Q.7, TP.HCM', tax_code='0314567890',
                status='active',
                notes='Nhà cung cấp bán thành phẩm: khung và vỏ cơ khí gia công sẵn',
            ),
            Supplier(
                id=6,
                name='Công ty TNHH Sản Phẩm Hoàn Thiện Thành Công',
                contact_person='Nguyễn Quốc Bảo', phone='0958345678',
                email='bao@thanhcong.vn',
                address='25 Đường Võ Văn Kiệt, Q.1, TP.HCM', tax_code='0315678901',
                status='active',
                notes='Nhà cung cấp thành phẩm: thiết bị hoàn thiện và hàng đóng gói sẵn',
            ),
        ]
        db.session.add_all(suppliers)
        db.session.commit()
        print(f"   ✅ {len(suppliers)} suppliers created")
        
        # Step 5: Insert categories
        print("4️⃣  Inserting categories...")
        categories = [
            Category(id=1, name='Nguyên liệu thô'),
            Category(id=2, name='Bán thành phẩm'),
            Category(id=3, name='Thành phẩm'),
        ]
        db.session.add_all(categories)
        db.session.commit()
        print(f"   ✅ {len(categories)} categories created")
        
        # Step 6: Insert goods
        print("5️⃣  Inserting goods...")
        goods_list = [
            Goods(id=1, sku='NL001', name='Hạt nhựa PP nguyên sinh', category_id=1, preferred_supplier_id=1,
                unit='Kg', min_stock=20, max_stock=200, quantity_on_hand=5, selling_price=42000.00,
                description='Nguyên liệu thô dùng ép vỏ và chi tiết nhựa'),
            Goods(id=2, sku='NL002', name='Phụ gia chống UV cho nhựa', category_id=1, preferred_supplier_id=1,
                unit='Kg', min_stock=10, max_stock=100, quantity_on_hand=12, selling_price=68000.00,
                description='Phụ gia nguyên liệu thô tăng độ bền màu sản phẩm'),
            Goods(id=3, sku='NL003', name='Thép cuộn cán nguội', category_id=1, preferred_supplier_id=2,
                unit='Kg', min_stock=15, max_stock=80, quantity_on_hand=3, selling_price=26500.00,
                description='Nguyên liệu thô cho gia công khung và vỏ cơ khí'),
            Goods(id=4, sku='NL004', name='Nhôm tấm 2mm', category_id=1, preferred_supplier_id=2,
                unit='Tấm', min_stock=10, max_stock=40, quantity_on_hand=16, selling_price=185000.00,
                description='Nguyên liệu thô dùng gia công mặt dựng thiết bị'),
            Goods(id=5, sku='NL005', name='Dung môi công nghiệp IPA', category_id=1, preferred_supplier_id=3,
                unit='Can', min_stock=20, max_stock=100, quantity_on_hand=25, selling_price=95000.00,
                description='Dung môi nguyên liệu thô dùng vệ sinh bề mặt'),
            Goods(id=6, sku='NL006', name='Chất đóng rắn epoxy', category_id=1, preferred_supplier_id=3,
                unit='Kg', min_stock=10, max_stock=50, quantity_on_hand=8, selling_price=145000.00,
                description='Hóa chất nguyên liệu thô dùng phối trộn keo epoxy'),
            Goods(id=7, sku='BTP001', name='Cụm mạch điều khiển nguồn', category_id=2, preferred_supplier_id=4,
                unit='Bộ', min_stock=5, max_stock=30, quantity_on_hand=0, selling_price=320000.00,
                description='Bán thành phẩm đã lắp linh kiện và kiểm tra chức năng'),
            Goods(id=8, sku='BTP002', name='Module hiển thị LCD 16x2', category_id=2, preferred_supplier_id=4,
                unit='Bộ', min_stock=10, max_stock=40, quantity_on_hand=16, selling_price=98000.00,
                description='Bán thành phẩm hiển thị dùng cho thiết bị hoàn chỉnh'),
            Goods(id=9, sku='BTP003', name='Khung thép sơn tĩnh điện', category_id=2, preferred_supplier_id=5,
                unit='Cái', min_stock=10, max_stock=40, quantity_on_hand=16, selling_price=285000.00,
                description='Bán thành phẩm cơ khí đã gia công và sơn hoàn thiện'),
            Goods(id=10, sku='BTP004', name='Vỏ nhôm gia công CNC', category_id=2, preferred_supplier_id=5,
                unit='Cái', min_stock=10, max_stock=50, quantity_on_hand=8, selling_price=410000.00,
                description='Bán thành phẩm vỏ nhôm đã cắt và xử lý bề mặt'),
            Goods(id=11, sku='TP001', name='Bộ điều khiển đóng gói hoàn chỉnh', category_id=3, preferred_supplier_id=6,
                unit='Bộ', min_stock=5, max_stock=30, quantity_on_hand=9, selling_price=1250000.00,
                description='Thành phẩm đã lắp ráp, kiểm thử và đóng gói'),
            Goods(id=12, sku='TP002', name='Thiết bị giám sát nhiệt độ', category_id=3, preferred_supplier_id=6,
                unit='Cái', min_stock=5, max_stock=25, quantity_on_hand=4, selling_price=890000.00,
                description='Thành phẩm sẵn sàng giao cho khách hàng'),
        ]
        db.session.add_all(goods_list)
        db.session.commit()
        print(f"   ✅ {len(goods_list)} goods created")

        # Step 6: Insert transactions for dashboard and feature demos
        print("6️⃣  Inserting purchase orders, receipts and issues...")
        today = datetime(2026, 8, 27, 9, 0, 0)
        purchase_orders = [
            PurchaseOrder(id=1, supplier_id=1, created_by=2,
                          order_date=datetime(2026, 8, 27, 8, 30),
                          status='chờ xác nhận', created_at=datetime(2026, 8, 27, 8, 30),
                          updated_at=datetime(2026, 8, 27, 8, 30)),
            PurchaseOrder(id=2, supplier_id=3, created_by=2,
                          order_date=datetime(2026, 8, 26, 14, 0),
                          status='đang giao', created_at=datetime(2026, 8, 26, 14, 0),
                          updated_at=datetime(2026, 8, 26, 14, 0)),
            PurchaseOrder(id=3, supplier_id=1, created_by=2,
                          order_date=datetime(2026, 8, 20, 10, 0),
                          status='đã nhận', created_at=datetime(2026, 8, 20, 10, 0),
                          updated_at=datetime(2026, 8, 22, 16, 0)),
        ]
        db.session.add_all(purchase_orders)
        db.session.flush()
        db.session.add_all([
            PurchaseOrderItem(po_id=1, goods_id=1, quantity_ordered=100, unit_price=2200),
            PurchaseOrderItem(po_id=1, goods_id=2, quantity_ordered=30, unit_price=68000),
            PurchaseOrderItem(po_id=2, goods_id=5, quantity_ordered=40, unit_price=95000),
            PurchaseOrderItem(po_id=2, goods_id=6, quantity_ordered=20, unit_price=145000),
            PurchaseOrderItem(po_id=3, goods_id=2, quantity_ordered=100, unit_price=1200),
        ])

        receipts = [
            GoodsReceipt(id=1, supplier_id=1, po_id=3, created_by=3,
                         received_date=datetime(2026, 8, 22, 15, 30),
                         note='Đã nhận đủ theo đơn đặt hàng PO-003',
                         created_at=datetime(2026, 8, 22, 15, 30),
                         updated_at=datetime(2026, 8, 22, 15, 30)),
            GoodsReceipt(id=2, supplier_id=3, po_id=2, created_by=3,
                         received_date=today,
                         note='Nhận đợt 1, còn thiếu một phần hóa chất',
                         created_at=today, updated_at=today),
            GoodsReceipt(id=3, supplier_id=1, po_id=None, created_by=3,
                         received_date=datetime(2026, 8, 27, 11, 15),
                         note='Nhập bổ sung hàng mẫu từ nhà cung cấp',
                         created_at=datetime(2026, 8, 27, 11, 15),
                         updated_at=datetime(2026, 8, 27, 11, 15)),
        ]
        db.session.add_all(receipts)
        db.session.flush()
        db.session.add_all([
            GoodsReceiptItem(receipt_id=1, goods_id=2, quantity=100, unit_price=1200),
            GoodsReceiptItem(receipt_id=2, goods_id=5, quantity=25, unit_price=95000),
            GoodsReceiptItem(receipt_id=2, goods_id=6, quantity=10, unit_price=145000),
            GoodsReceiptItem(receipt_id=3, goods_id=1, quantity=20, unit_price=2200),
        ])

        issues = [
            GoodsIssue(id=1, created_by=3, issued_date=datetime(2026, 8, 27, 10, 0),
                       note='Xuất văn phòng phẩm cho phòng hành chính',
                       created_at=datetime(2026, 8, 27, 10, 0),
                       updated_at=datetime(2026, 8, 27, 10, 0)),
            GoodsIssue(id=2, created_by=3, issued_date=datetime(2026, 8, 27, 14, 20),
                       note='Xuất linh kiện cho bộ phận kỹ thuật',
                       created_at=datetime(2026, 8, 27, 14, 20),
                       updated_at=datetime(2026, 8, 27, 14, 20)),
            GoodsIssue(id=3, created_by=3, issued_date=datetime(2026, 8, 25, 9, 45),
                       note='Xuất vật tư cho đơn hàng sản xuất SP-026',
                       created_at=datetime(2026, 8, 25, 9, 45),
                       updated_at=datetime(2026, 8, 25, 9, 45)),
        ]
        db.session.add_all(issues)
        db.session.flush()
        db.session.add_all([
            GoodsIssueItem(issue_id=1, goods_id=5, quantity=5),
            GoodsIssueItem(issue_id=1, goods_id=4, quantity=2),
            GoodsIssueItem(issue_id=2, goods_id=2, quantity=3),
            GoodsIssueItem(issue_id=2, goods_id=1, quantity=1),
            GoodsIssueItem(issue_id=3, goods_id=3, quantity=1),
        ])

        stocktakes = [
            Stocktake(id=1, created_by=3, approved_by=2,
                      stocktake_date=datetime(2026, 8, 18, 9, 0), status='đã phê duyệt',
                      note='Kiểm kê định kỳ tháng 8', created_at=datetime(2026, 8, 18, 9, 0),
                      updated_at=datetime(2026, 8, 19, 16, 0)),
            Stocktake(id=2, created_by=3, approved_by=None,
                      stocktake_date=datetime(2026, 8, 27, 8, 0), status='chờ phê duyệt',
                      note='Kiểm kê nhanh khu vực linh kiện', created_at=datetime(2026, 8, 27, 8, 0),
                      updated_at=datetime(2026, 8, 27, 8, 0)),
        ]
        db.session.add_all(stocktakes)
        db.session.flush()
        db.session.add_all([
            StocktakeItem(stocktake_id=1, goods_id=5, system_quantity=25, actual_quantity=25,
                          difference=0, action='Không có chênh lệch'),
            StocktakeItem(stocktake_id=1, goods_id=4, system_quantity=50, actual_quantity=48,
                          difference=-2, action='Đã cập nhật hao hụt'),
            StocktakeItem(stocktake_id=2, goods_id=1, system_quantity=5, actual_quantity=4,
                          difference=-1, action='Tìm nguyên nhân thiếu hàng'),
            StocktakeItem(stocktake_id=2, goods_id=3, system_quantity=3, actual_quantity=3,
                          difference=0, action='Không có chênh lệch'),
        ])

        invoices = [
            SupplierInvoice(id=1, supplier_id=1, receipt_id=1, invoice_number='INV-TL-0822',
                            issue_date=datetime(2026, 8, 22), total_amount=120000,
                            payment_status='đã thanh toán', created_at=datetime(2026, 8, 22),
                            updated_at=datetime(2026, 8, 23)),
            SupplierInvoice(id=2, supplier_id=3, receipt_id=2, invoice_number='INV-MP-0827',
                            issue_date=datetime(2026, 8, 27), total_amount=3550000,
                            payment_status='thanh toán một phần', created_at=today, updated_at=today),
        ]
        db.session.add_all(invoices)
        db.session.flush()
        db.session.add_all([
            SupplierPayment(invoice_id=1, amount=120000, payment_date=datetime(2026, 8, 23),
                            method='chuyển khoản'),
            SupplierPayment(invoice_id=2, amount=1500000, payment_date=datetime(2026, 8, 27),
                            method='chuyển khoản'),
        ])

        # Add a wider transaction history for reports and list pages.
        extra_dates = [
            datetime(2025, 1, 14, 9, 0), datetime(2025, 4, 22, 10, 30),
            datetime(2025, 7, 9, 14, 0), datetime(2025, 10, 18, 8, 45),
            datetime(2025, 12, 5, 15, 15), datetime(2026, 1, 20, 9, 30),
            datetime(2026, 2, 17, 11, 0), datetime(2026, 3, 28, 13, 45),
            datetime(2026, 5, 12, 10, 15), datetime(2026, 7, 24, 16, 0),
        ]
        extra_orders = []
        extra_order_items = []
        extra_receipts = []
        extra_receipt_items = []
        extra_issues = []
        extra_issue_items = []
        extra_stocktakes = []
        extra_stocktake_items = []
        extra_invoices = []
        extra_payments = []
        order_statuses = ['đã nhận', 'đang giao', 'đã xác nhận', 'hủy', 'đã nhận']
        payment_methods = ['chuyển khoản', 'tiền mặt', 'ủy nhiệm chi']

        for offset, event_date in enumerate(extra_dates, start=1):
            po_id = 3 + offset
            receipt_id = 3 + offset
            issue_id = 3 + offset
            stocktake_id = 2 + offset
            invoice_id = 2 + offset
            goods_id = ((offset - 1) % 12) + 1
            supplier_id = {
                1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3,
                7: 4, 8: 4, 9: 5, 10: 5, 11: 6, 12: 6,
            }[goods_id]
            status = order_statuses[(offset - 1) % len(order_statuses)]

            extra_orders.append(PurchaseOrder(
                id=po_id, supplier_id=supplier_id, created_by=2,
                order_date=event_date, status=status,
                created_at=event_date, updated_at=event_date,
            ))
            extra_order_items.append(PurchaseOrderItem(
                po_id=po_id, goods_id=goods_id,
                quantity_ordered=20 + offset * 5, unit_price=1000 + offset * 500,
            ))
            extra_receipts.append(GoodsReceipt(
                id=receipt_id, supplier_id=supplier_id, po_id=po_id, created_by=3,
                received_date=event_date, note=f'Nhập hàng đợt {offset:02d} theo PO-{po_id:03d}',
                created_at=event_date, updated_at=event_date,
            ))
            extra_receipt_items.append(GoodsReceiptItem(
                receipt_id=receipt_id, goods_id=goods_id,
                quantity=15 + offset, unit_price=1000 + offset * 500,
            ))
            extra_issues.append(GoodsIssue(
                id=issue_id, created_by=3, issued_date=event_date,
                note=f'Xuất hàng cho bộ phận sử dụng đợt {offset:02d}',
                created_at=event_date, updated_at=event_date,
            ))
            extra_issue_items.append(GoodsIssueItem(
                issue_id=issue_id, goods_id=goods_id, quantity=1 + (offset % 4),
            ))
            difference = -1 if offset % 3 == 0 else (1 if offset % 3 == 1 else 0)
            extra_stocktakes.append(Stocktake(
                id=stocktake_id, created_by=3, approved_by=2 if offset % 2 else None,
                stocktake_date=event_date,
                status='đã phê duyệt' if offset % 2 else 'chờ phê duyệt',
                note=f'Kiểm kê khu vực hàng hóa đợt {offset:02d}',
                created_at=event_date, updated_at=event_date,
            ))
            extra_stocktake_items.append(StocktakeItem(
                stocktake_id=stocktake_id, goods_id=goods_id,
                system_quantity=20 + offset, actual_quantity=20 + offset + difference,
                difference=difference,
                action='Đã cập nhật chênh lệch' if difference else 'Không có chênh lệch',
            ))
            total_amount = float((15 + offset) * (1000 + offset * 500))
            paid_amount = total_amount if offset % 3 == 0 else total_amount / 2
            extra_invoices.append(SupplierInvoice(
                id=invoice_id, supplier_id=supplier_id, receipt_id=receipt_id,
                invoice_number=f'INV-SEED-{invoice_id:03d}', issue_date=event_date,
                total_amount=total_amount,
                payment_status='đã thanh toán' if offset % 3 == 0 else 'thanh toán một phần',
                created_at=event_date, updated_at=event_date,
            ))
            extra_payments.append(SupplierPayment(
                invoice_id=invoice_id, amount=paid_amount,
                payment_date=event_date, method=payment_methods[(offset - 1) % 3],
            ))

        db.session.add_all(extra_orders + extra_receipts + extra_issues + extra_stocktakes + extra_invoices)
        db.session.flush()
        db.session.add_all(
            extra_order_items + extra_receipt_items + extra_issue_items
            + extra_stocktake_items + extra_payments
        )
        db.session.commit()
        print('   ✅ 13 purchase orders, 13 receipts, 13 issues, 12 stocktakes and 12 invoices created')
        
        print("\n✅ Database seeding completed successfully!")
        print(f"\nTest Accounts:")
        for u in users:
            print(f"  • {u.username} / Password@123 (role: {u.role})")

if __name__ == '__main__':
    seed_database()
