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
                name='Công ty TNHH Phụ Tùng Thiên Long',
                contact_person='Phạm Minh Đức',
                phone='0901234567',
                email='duc.pham@thienlong.vn',
                address='123 Đường Lý Thường Kiệt, Q.10, TP.HCM',
                tax_code='0312345678',
                status='active',
                notes='NCC ưu tiên cho linh kiện điện tử',
            ),
            Supplier(
                id=2,
                name='HTX Sản Xuất Văn Phòng Phẩm Bình Dương',
                contact_person='Nguyễn Thị Hoa',
                phone='0912345678',
                email='hoa.nt@vppbinhduong.vn',
                address='45 Đường Trần Phú, TX.Thủ Dầu Một, Bình Dương',
                tax_code='3702345678',
                status='active',
                notes='Chuyên cung cấp văn phòng phẩm, giao hàng mỗi thứ 2',
            ),
            Supplier(
                id=3,
                name='Công ty CP Thiết Bị Bảo Hộ An Toàn Việt',
                contact_person='Trần Quốc Hùng',
                phone='0987654321',
                email='hung.tq@baohoanviet.vn',
                address='789 Đường Cộng Hòa, Q.Tân Bình, TP.HCM',
                tax_code='0312987654',
                status='inactive',
                notes='Tạm ngừng hợp tác từ 2026-06 do giao hàng chậm',
            ),
        ]
        db.session.add_all(suppliers)
        db.session.commit()
        print(f"   ✅ {len(suppliers)} suppliers created")
        
        # Step 5: Insert categories
        print("4️⃣  Inserting categories...")
        categories = [
            Category(id=1, name='Linh kiện điện tử'),
            Category(id=2, name='Văn phòng phẩm'),
            Category(id=3, name='Thiết bị bảo hộ'),
        ]
        db.session.add_all(categories)
        db.session.commit()
        print(f"   ✅ {len(categories)} categories created")
        
        # Step 6: Insert goods
        print("5️⃣  Inserting goods...")
        goods_list = [
            Goods(id=1, sku='SKU001', name='Tụ điện 100μF 25V', category_id=1, preferred_supplier_id=1, 
                  unit='Cái', min_stock=20, max_stock=200, quantity_on_hand=5, selling_price=15000.00,
                  description='Tụ điện hóa học loại tốt, chịu được 25V'),
            Goods(id=2, sku='SKU002', name='Điện trở 1K 1/4W', category_id=1, preferred_supplier_id=1,
                  unit='Cái', min_stock=10, max_stock=500, quantity_on_hand=12, selling_price=1500.00,
                  description='Điện trở film mỏng chính xác'),
            Goods(id=3, sku='SKU003', name='Led xanh 5mm', category_id=1, preferred_supplier_id=1,
                  unit='Cái', min_stock=15, max_stock=1000, quantity_on_hand=3, selling_price=2000.00,
                  description='Led xanh độ sáng cao'),
            Goods(id=4, sku='SKU004', name='Bút chì HB', category_id=2, preferred_supplier_id=2,
                  unit='Cái', min_stock=50, max_stock=40, quantity_on_hand=50, selling_price=3000.00,
                  description='Bút chì gỗ chất lượng tốt'),
            Goods(id=5, sku='SKU005', name='Giấy A4 80gsm', category_id=2, preferred_supplier_id=2,
                  unit='Ream', min_stock=20, max_stock=100, quantity_on_hand=25, selling_price=80000.00,
                  description='Giấy in trắng tiêu chuẩn A4'),
            Goods(id=6, sku='SKU006', name='Mực in đen HP', category_id=2, preferred_supplier_id=2,
                  unit='Hộp', min_stock=10, max_stock=50, quantity_on_hand=8, selling_price=150000.00,
                  description='Mực in laser màu đen'),
            Goods(id=7, sku='SKU007', name='Mũ bảo hộ', category_id=3, preferred_supplier_id=3,
                  unit='Cái', min_stock=5, max_stock=50, quantity_on_hand=0, selling_price=50000.00,
                  description='Mũ bảo hộ lao động tiêu chuẩn'),
            Goods(id=8, sku='SKU008', name='Găng tay cao su', category_id=3, preferred_supplier_id=3,
                  unit='Hộp', min_stock=10, max_stock=150, quantity_on_hand=200, selling_price=80000.00,
                  description='Găng tay cao su chống hóa chất'),
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
            PurchaseOrder(id=2, supplier_id=2, created_by=2,
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
            PurchaseOrderItem(po_id=1, goods_id=3, quantity_ordered=30, unit_price=115000),
            PurchaseOrderItem(po_id=2, goods_id=5, quantity_ordered=40, unit_price=76000),
            PurchaseOrderItem(po_id=2, goods_id=6, quantity_ordered=20, unit_price=165000),
            PurchaseOrderItem(po_id=3, goods_id=2, quantity_ordered=100, unit_price=1200),
        ])

        receipts = [
            GoodsReceipt(id=1, supplier_id=1, po_id=3, created_by=3,
                         received_date=datetime(2026, 8, 22, 15, 30),
                         note='Đã nhận đủ theo đơn đặt hàng PO-003',
                         created_at=datetime(2026, 8, 22, 15, 30),
                         updated_at=datetime(2026, 8, 22, 15, 30)),
            GoodsReceipt(id=2, supplier_id=2, po_id=2, created_by=3,
                         received_date=today,
                         note='Nhận đợt 1, còn thiếu một phần mực in',
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
            GoodsReceiptItem(receipt_id=2, goods_id=5, quantity=25, unit_price=76000),
            GoodsReceiptItem(receipt_id=2, goods_id=6, quantity=10, unit_price=165000),
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
            SupplierInvoice(id=2, supplier_id=2, receipt_id=2, invoice_number='INV-BD-0827',
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
            goods_id = (offset % 8) + 1
            supplier_id = 1 if offset % 2 else 2
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
