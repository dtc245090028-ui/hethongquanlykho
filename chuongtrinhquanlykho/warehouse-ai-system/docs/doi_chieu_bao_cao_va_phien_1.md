# Bao cao hien trang he thong quan ly kho

Ngay cap nhat: 2026-08-27

Tai lieu nay ghi lai trang thai thuc te cua project sau khi doi chieu truc tiep voi backend, frontend, test va cac tai lieu trong project.

## 1. Da co trong he thong

### Backend va co so du lieu

- Flask application factory tai `backend/app/main.py`.
- SQLAlchemy va SQLite; cac model hien co:
  - `User`
  - `Supplier`
  - `Category`
  - `Goods`
  - `PurchaseOrder`, `PurchaseOrderItem`
  - `GoodsReceipt`, `GoodsReceiptItem`
  - `GoodsIssue`, `GoodsIssueItem`
  - `Stocktake`, `StocktakeItem`
  - `SupplierInvoice`, `SupplierPayment`
  - `AIInteractionLog`
- Auth JWT va bcrypt: dang nhap, dang xuat, lay user hien tai va phan quyen ba role `admin`, `warehouse_manager`, `warehouse_keeper`.
- Router da dang ky:
  - `/api/auth`
  - `/api/users` (quan tri tai khoan, chi admin)
  - `/api/categories` (danh sach, them, sua danh muc)
  - `/api/suppliers`
  - `/api/goods`
  - `/api/purchase-orders`
  - `/api/goods-receipts`
  - `/api/goods-issues`
  - `/api/stocktakes`
  - `/api/supplier-invoices`
  - `/api/supplier-payments`
  - `/api/reports`
  - `/api/ai`
- Nghiep vu ton kho da co: nhap kho cap nhat ton trong transaction, xuat kho chan vuot ton, kiem ke theo luong de xuat -> phe duyet -> cap nhat ton, luu snapshot gia nhap, hoa don va thanh toan nha cung cap.
- Phieu nhap theo PO da doi chieu tong so luong da nhan voi so luong dat, tu choi nhan vuot PO.
- Quan tri user da co CRUD co ban, khoa tai khoan, doi role va hash password.
- Quan ly category da co API list/detail/create/update va chan ten trung Unicode.
- Bao cao da co: gia tri ton kho, vong quay va hang cham luan chuyen, top hang nhap/xuat, chenh lech kiem ke.
- AI da co: bao cao ton kho, goi y dat hang lai, luu log tuong tac va scheduler quet hang duoi muc toi thieu.

### Frontend HTML, JS va CSS

- Trang dang nhap: `frontend/index.html`.
- Dashboard: `frontend/dashboard.html`.
- Trang nghiep vu da co:
  - `pages/goods.html`
  - `pages/suppliers.html`
  - `pages/purchase-orders.html`
  - `pages/goods-receipts.html`
  - `pages/goods-issues.html`
  - `pages/stocktakes.html`
  - `pages/invoices.html`
  - `pages/reports.html`
  - `pages/ai-features.html`
- JavaScript dung chung: `js/api.js`, `js/auth.js`, `js/layout.js`, `js/utils.js`.
- CSS dung chung: `css/style.css`.
- Dockerfile va Nginx reverse proxy da co.

### Test va van hanh

- Test module da co cho Auth, AI, Goods, Goods Issues, Goods Receipts, Purchase Orders, Reports, Stocktakes, Suppliers va Supplier Invoices.
- Ket qua da xac nhan:
  - Auth + AI: `15 passed`.
  - Auth + xuat kho + kiem ke: `34 passed`.
  - Categories + users: `6 passed`.
  - Goods receipts + categories + users: `30 passed`.
- Da bo sung `marshmallow-sqlalchemy` vao `requirements.txt`.
- Da thay `datetime.utcnow()` bang ham UTC hien dai trong cac model.
- Da thay `Query.get()` con lai trong test bang `db.session.get()`.
- CORS doc tu bien moi truong `CORS_ORIGINS`; JWT secret development da du do dai.
- Huong dan chay he thong co trong `README.md` va `docker-compose.yml`.

## 2. Con thieu hoac can hoan thien

### Uu tien cao

1. Chua co giao dien frontend rieng cho quan tri user va quan ly category.
2. Chua co `AuditLog` cho tao/huy phieu, phe duyet kiem ke va thanh toan; hien chi co `AIInteractionLog`.
3. `backend/app/schemas/__init__.py` moi la package placeholder, chua co schema validate rieng cho payload giao dich.

### Uu tien trung binh

- AI inventory report moi phan tich snapshot tu `Goods`, chua tong hop day du lich su nhap/xuat.
- `AI_PROVIDER` chua duoc tach thanh adapter; service dang phu thuoc Gemini.
- Loi AI o service van co the ghi chi tiet exception; nen tra thong bao co dinh cho client va chi log chi tiet o server.
- Scheduler moi ghi log hang ton thap, chua co thong bao in-app/email.
- Chua co workflow thanh ly hang hong hoac het han rieng.

### Uu tien thap va tai lieu ban giao

- Chua co script backup/restore SQLite chinh thuc.
- Can thong nhat mot vi tri database chuan cho local va Docker.
- Can bo sung tai lieu thiet ke, use case, ERD va final report neu do an yeu cau.
- Can kiem thu frontend theo tung trang voi backend, khong chi kiem tra file HTML ton tai.
- Can chay va ghi nhan day du toan bo test trong `docs/test_report.md`.

## 3. Cach khoi dong hien tai

### Docker

Tu thu muc `warehouse-ai-system`:

```powershell
Copy-Item backend\.env.example backend\.env
docker compose up --build
docker exec warehouse-backend sh /app/scripts/seed_docker.sh
```

- Frontend: `http://localhost`
- Backend API: `http://localhost:5000`
- Dien `SECRET_KEY` va `GEMINI_API_KEY` trong `backend/.env`.

### Chay local

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
flask --app app run --debug
```

Frontend co the mo bang Nginx/Docker; neu mo file HTML truc tiep thi backend van phai dang chay tai port 5000 va CORS phai cho phep origin tuong ung.

## 4. Ket luan

He thong da co MVP cho dang nhap, hang hoa, nha cung cap, nhap, xuat, kiem ke, cong no, bao cao, AI va giao dien HTML. He thong chua hoan tat 100% cho ban nghiem thu vi con thieu quan ly user, danh muc, audit log, doi chieu PO va validate input tap trung. Thu tu nen lam tiep la: categories/users, audit log, doi chieu PO, schemas, sau do mo rong AI va tai lieu ban giao.
