# Phan bo he thong quan ly kho

## 1. Tong quan luong hoat dong

```text
Nguoi dung
    |
    v
Frontend: HTML / CSS / JavaScript
    |
    | Goi API HTTP
    v
Backend: Flask API
    |
    v
Database: SQLite
    |
    v
AI Gemini (chi dung cho bao cao va goi y)
```

He thong duoc chia thanh cac lop:

- **Frontend** hien thi giao dien va nhan thao tac tu nguoi dung.
- **Backend** xu ly dang nhap, phan quyen va nghiep vu quan ly kho.
- **Database** luu tai khoan, hang hoa, phieu nhap, phieu xuat, kiem ke va cong no.
- **AI** phan tich du lieu ton kho, tao bao cao va goi y nhap hang.
- **Docker/Nginx** dong goi, khoi dong va ket noi frontend voi backend.

## 2. Frontend: giao dien web

Thu muc: `frontend/`

| Thanh phan | Phu trach |
|---|---|
| `index.html` | Trang dang nhap |
| `dashboard.html` | Trang tong quan sau khi dang nhap |
| `pages/goods.html` | Quan ly hang hoa |
| `pages/suppliers.html` | Quan ly nha cung cap |
| `pages/purchase-orders.html` | Quan ly don dat hang |
| `pages/goods-receipts.html` | Quan ly phieu nhap kho |
| `pages/goods-issues.html` | Quan ly phieu xuat kho |
| `pages/stocktakes.html` | Quan ly kiem ke kho |
| `pages/invoices.html` | Quan ly hoa don va cong no |
| `pages/reports.html` | Bao cao thong ke |
| `pages/ai-features.html` | Cac chuc nang AI |
| `css/style.css` | Mau sac, bo cuc va giao dien |

### JavaScript dung chung

| File | Phu trach |
|---|---|
| `js/api.js` | Goi API backend, gui JWT va xu ly loi |
| `js/auth.js` | Kiem tra dang nhap, dang xuat va thong tin quyen |
| `js/layout.js` | Render menu trai, topbar va dieu huong |
| `js/utils.js` | Dinh dang tien/ngay, toast, hop xac nhan va phan trang |

## 3. Backend: Flask API

Thu muc: `backend/app/`

| Thanh phan | Phu trach |
|---|---|
| `main.py` | Tao ung dung Flask va dang ky toan bo blueprint/API |
| `extensions.py` | Khoi tao SQLAlchemy, JWT va Marshmallow |
| `auth/` | Dang nhap, dang xuat, xac thuc JWT va phan quyen |
| `routers/users.py` | Quan ly nguoi dung |
| `routers/categories.py` | Quan ly danh muc |
| `routers/suppliers.py` | Quan ly nha cung cap |
| `routers/goods.py` | Quan ly hang hoa va ton kho |
| `routers/purchase_orders.py` | Quan ly don dat hang |
| `routers/goods_receipts.py` | Xu ly phieu nhap kho |
| `routers/goods_issues.py` | Xu ly phieu xuat kho |
| `routers/stocktakes.py` | Xu ly kiem ke kho |
| `routers/supplier_invoices.py` | Xu ly hoa don va thanh toan |
| `routers/reports.py` | Tao du lieu bao cao |
| `routers/ai_features.py` | API goi chuc nang AI |

Router la noi tiep nhan request tu frontend, kiem tra quyen, xu ly nghiep vu va tra response JSON.

## 4. Model va database

Thu muc model: `backend/app/models/`

| Model | Du lieu phu trach |
|---|---|
| `user.py` | Tai khoan va role |
| `category.py` | Danh muc hang hoa |
| `supplier.py` | Nha cung cap |
| `goods.py` | Hang hoa, so luong ton va gia |
| `purchase_order.py` | Don dat hang |
| `goods_receipt.py` | Phieu nhap va chi tiet phieu nhap |
| `goods_issue.py` | Phieu xuat va chi tiet phieu xuat |
| `stocktake.py` | Phieu kiem ke va chi tiet kiem ke |
| `supplier_invoice.py` | Hoa don va thanh toan nha cung cap |
| `ai_interaction_log.py` | Lich su tuong tac voi AI |

File `models/__init__.py` import cac model de SQLAlchemy biet va tao cac bang database khi ung dung khoi dong.

Database phat trien thuong nam tai `backend/instance/warehouse.db`. Khi chay Docker, database duoc luu trong volume `db_data`.

## 5. Phan AI

Thu muc: `backend/app/ai/`

| Thanh phan | Phu trach |
|---|---|
| `inventory_report_service.py` | Sinh bao cao ton kho bang AI |
| `reorder_suggestion_service.py` | Goi y nhap them hang |
| `scheduler.py` | Chay kiem tra/gian doan xu ly dinh ky |
| `prompts/` | Cac prompt gui cho Gemini |

AI la lop ho tro, khong phai nghiep vu cot loi. Neu AI khong hoat dong, cac nghiep vu nhap, xuat, ton va kiem ke van phai tiep tuc hoat dong.

## 6. Phan chay he thong

| File | Phu trach |
|---|---|
| `docker-compose.yml` | Khoi dong frontend, backend va volume database |
| `frontend/Dockerfile` | Tao container Nginx phuc vu web |
| `frontend/nginx.conf` | Phuc vu file tinh va chuyen request `/api/` sang backend |
| `backend/Dockerfile` | Tao container Flask |
| `backend/.env` | Cau hinh secret key, database va Gemini API key |
| `backend/requirements.txt` | Danh sach thu vien Python cho backend |

Khi chay Docker, dia chi giao dien la `http://localhost` va backend truc tiep la `http://localhost:5000`.

## 7. Du lieu mau, kiem thu va tai lieu

| Thanh phan | Phu trach |
|---|---|
| `database/seed_data.sql` | Du lieu mau bang SQL |
| `backend/seed_database.py` | Tao du lieu mau bang Python |
| `backend/tests/` | Kiem thu API va nghiep vu |
| `backend/check_db_uri.py` | Kiem tra dia chi database |
| `backend/check_tables.py` | Kiem tra bang database |
| `backend/check_users.py` | Kiem tra tai khoan |
| `docs/` | Tai lieu thiet ke, API, AI va ket qua test |

## 8. Muc do anh huong neu xoa

### 8.1. Loi rat lon: he thong co the khong khoi dong

Khong nen xoa cac thanh phan sau:

- `backend/app/main.py`: Flask khong tao duoc ung dung.
- `backend/app/extensions.py`: Khong khoi tao duoc database, JWT va Marshmallow.
- `backend/app/models/__init__.py`: Model khong duoc nap, bang co the khong duoc tao.
- Bat ky file nao trong `backend/app/routers/`: `main.py` import va dang ky router khi khoi dong; xoa mot router co the lam toan bo backend loi.
- Bat ky model nao duoc import trong `backend/app/models/__init__.py`: Co the gay loi import hoac thieu bang/quan he database.
- `backend/Dockerfile`: Khong build duoc container backend.
- `frontend/Dockerfile`: Khong build duoc container frontend.
- `frontend/index.html`: Khong con trang dang nhap.
- `frontend/js/api.js`: Phan lon trang sau dang nhap khong goi duoc API.

### 8.2. Loi vua: mat mot trang hoac mot chuc nang

- Xoa mot file trong `frontend/pages/`: Trang tuong ung bi loi 404.
- Xoa `frontend/js/auth.js`: Dang nhap, dang xuat va phan quyen tren giao dien bi loi.
- Xoa `frontend/js/layout.js`: Mat menu, topbar va dieu huong.
- Xoa `frontend/js/utils.js`: Cac ham dinh dang, thong bao va hop xac nhan bi loi.
- Xoa `frontend/css/style.css`: Web van co the chay nhung giao dien bi mat.
- Xoa mot service AI: Chuc nang AI tuong ung bi loi, nhung nghiep vu kho co the van chay.
- Xoa `database/seed_data.sql` hoac `backend/seed_database.py`: Khong con cach nap du lieu mau tuong ung.

### 8.3. Mat du lieu

- Xoa `backend/instance/warehouse.db`: Du lieu SQLite cu bi mat; code co the tao lai database rong.
- Chay `docker compose down -v`: Xoa volume `db_data` va mat du lieu Docker.
- Xoa file `.env` that: Ung dung co the khong co secret key hoac Gemini API key can thiet.

### 8.4. Co the xoa neu chap nhan mat tai lieu/cong cu

- `docs/`: Ung dung van co the chay nhung mat tai lieu.
- `backend/tests/`: Ung dung van co the chay nhung mat bo kiem thu.
- Cac file `check_*.py`: Chi la cong cu kiem tra, khong phai luong chay chinh.
- `frontend/.gitkeep`: Khong anh huong den viec chay web.
- `.dockerignore`: Thuong khong lam ung dung loi truc tiep, nhung co the lam Docker copy them file khong can thiet.

## 9. Luu y cau hinh API

`frontend/js/api.js` va mot so doan trong `frontend/index.html`, `frontend/js/auth.js` dang goi truc tiep `http://localhost:5000/api`.

Trong khi do, `frontend/nginx.conf` duoc cau hinh de chuyen tiep request `/api/` qua service backend. Khi chay Docker, nen thong nhat frontend goi `/api` de tan dung reverse proxy Nginx va tranh phu thuoc vao hostname/port localhost cua may nguoi dung.

## 10. Ket luan

- Frontend hien thi giao dien va gui thao tac.
- Backend xu ly xac thuc, phan quyen va nghiep vu.
- Router cung cap API theo tung module.
- Model mo ta du lieu va quan he database.
- Database luu tru du lieu he thong.
- AI tao bao cao va goi y, khong thay the nghiep vu kho.
- Docker va Nginx ket noi, dong goi va phuc vu he thong.
