#!/usr/bin/env python
"""
seed_database.py — Khởi tạo database với seed data
Chạy: python seed_database.py
"""
import sys
import os

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
        
        print("\n✅ Database seeding completed successfully!")
        print(f"\nTest Accounts:")
        for u in users:
            print(f"  • {u.username} / Password@123 (role: {u.role})")

if __name__ == '__main__':
    seed_database()
