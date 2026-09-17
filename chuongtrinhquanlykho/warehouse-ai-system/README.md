# Chạy nhanh bằng VS Code

Workspace đã có cấu hình `.vscode/launch.json` (nằm ở **thư mục gốc project**, không phải trong `warehouse-ai-system/`) để chạy không cần gõ lệnh thủ công:

1. Mở thanh **Run and Debug** (`Ctrl+Shift+D`).
2. Chọn `Warehouse System (API + Frontend)`.
3. Bấm `F5`.

Cấu hình này chạy Flask API tại `http://localhost:5000` và frontend static tại
`http://localhost:5500`. Trình duyệt sẽ tự mở trang frontend. Cần tạo
`backend/.env` trước nếu dùng AI/Gemini.

> Kiến trúc hiện tại giữ nguyên Flask + HTML/JS + Bootstrap theo đặc tả đồ án.
> Frontend có `package.json` riêng để cung cấp lệnh chạy static server, nhưng
> không phải ứng dụng React và backend không phải Express.

---

# Hệ thống quản lý kho có tích hợp AI

Đồ án môn học — Hệ thống quản lý hàng hóa, nhà cung cấp, phiếu nhập/xuất và tồn kho, tích hợp AI sinh báo cáo và gợi ý nhập hàng.

## Stack

| Lớp | Công nghệ |
|---|---|
| Backend | Flask (Python 3.10+) |
| Frontend | HTML/JS + Bootstrap, static server |
| CSDL | SQLite (dev/demo) |
| AI | Gemini API (có thể đổi qua `.env`) |

---

## Chức năng hệ thống

### Quản lý nghiệp vụ kho

| Module | Mô tả | Endpoint chính |
|---|---|---|
| **Xác thực** | Đăng nhập JWT, phân quyền 3 role | `/api/auth/login`, `/api/auth/me` |
| **Người dùng** | CRUD tài khoản (admin) | `/api/users` |
| **Nhóm hàng** | Quản lý danh mục hàng hóa | `/api/categories` |
| **Hàng hóa** | Quản lý mặt hàng, tồn kho, tồn tối thiểu | `/api/goods` |
| **Nhà cung cấp** | Quản lý thông tin NCC | `/api/suppliers` |
| **Đơn đặt hàng** | Tạo và theo dõi đơn đặt hàng NCC | `/api/purchase-orders` |
| **Phiếu nhập kho** | Lập phiếu nhập, cập nhật tồn kho | `/api/goods-receipts` |
| **Phiếu xuất kho** | Lập phiếu xuất, kiểm tra tồn | `/api/goods-issues` |
| **Kiểm kê kho** | Đề xuất → Phê duyệt → Cập nhật tồn | `/api/stocktakes` |
| **Hóa đơn NCC** | Theo dõi công nợ, thanh toán nhà cung cấp | `/api/supplier-invoices`, `/api/supplier-payments` |
| **Báo cáo** | Giá trị tồn kho, vòng quay, top hàng, chênh lệch kiểm kê | `/api/reports/*` |

### Cổng đối tác (ngoài tài khoản nội bộ)

| Module | Mô tả | Endpoint chính |
|---|---|---|
| **Cổng nhà cung cấp** | NCC tự đăng nhập bằng số điện thoại, xem catalog và gửi bảng chào giá | `/api/supplier-portal/*` |
| **Cổng khách hàng** | Khách hàng đặt mua hàng không cần tài khoản, bộ phận kho xác nhận | `/api/buyer-portal/*` |

### Chức năng AI (Gemini API)

| Tính năng | Mô tả | Endpoint |
|---|---|---|
| **Báo cáo tồn kho** | AI phân tích tình trạng tồn kho toàn bộ hàng hóa | `POST /api/ai/inventory-report` |
| **Gợi ý nhập hàng** | AI đề xuất hàng cần nhập dựa trên tồn và tốc độ xuất 30 ngày | `POST /api/ai/reorder-suggestion` |
| **Scheduler ngầm** | Tự động kiểm tra tồn kho theo lịch, cảnh báo hàng dưới tồn tối thiểu | Chạy nền khi khởi động app |

### Phân quyền

| Role | Tên trong hệ thống | Quyền hạn chính |
|---|---|---|
| Ban điều hành | `admin` | Toàn quyền, quản lý người dùng |
| Quản lý kho | `warehouse_manager` | Duyệt kiểm kê, xem báo cáo, dùng AI |
| Thủ kho | `warehouse_keeper` | Lập phiếu nhập/xuất, đề xuất kiểm kê |
| Nhà cung cấp | `supplier` | Chỉ dùng được Supplier Portal |

---

## Cài đặt & Chạy

### Cấu trúc chạy local

Mở hai terminal tại thư mục `warehouse-ai-system/`.

**Terminal 1 — Backend Flask (port 5000):**

```bash
cd backend
python -m venv venv

# Windows PowerShell
venv\Scripts\Activate.ps1

# Linux / macOS
# source venv/bin/activate

pip install -r requirements.txt
flask --app app.main run --debug --port 5000
```

**Terminal 2 — Frontend static (port 5500):**

```bash
cd frontend
npm run dev
```

Lệnh `npm run dev` gọi `python -m http.server 5500` thông qua
`frontend/package.json`, không cần cài dependency Node.js.

Mở frontend tại: `http://localhost:5500/index.html`.
API chạy tại: `http://localhost:5000/api`.

Khi frontend chạy ở port `5500`, các request API sẽ gọi trực tiếp Flask ở
port `5000`. Khi chạy qua Docker/Nginx, frontend tự chuyển sang gọi `/api` và
Nginx proxy request tới backend.

### 1. Vào thư mục backend

```bash
cd backend/
```

### 2. Tạo virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Cài thư viện

```bash
pip install -r requirements.txt
```

### 4. Tạo file .env

```bash
cp .env.example .env
# Sau đó mở .env và điền SECRET_KEY + GEMINI_API_KEY
```

Các biến quan trọng trong `.env`:

```env
SECRET_KEY=<chuỗi ngẫu nhiên dài>
GEMINI_API_KEY=<key Gemini của bạn>
AI_MODEL=gemini-1.5-flash
DATABASE_URL=sqlite:///./warehouse.db   # mặc định SQLite
```

### 5. Chạy server

```bash
# Cách 1: Flask CLI
flask --app app run --debug

# Cách 2: Python trực tiếp
python -m app.main
```

Server chạy tại: http://localhost:5000

### 6. Seed dữ liệu mẫu

```bash
# Từ thư mục backend/ (sau khi đã chạy server ít nhất 1 lần để tạo DB)
python seed_database.py
```

> **Lưu ý**: Chạy server ít nhất một lần trước khi seed để Flask tự tạo file
> `backend/instance/warehouse.db`. Password mẫu của cả 3 tài khoản: `Password@123`

### 7. Chạy test

```bash
# Từ thư mục backend/
pytest tests/ -v
```

---

## Tài khoản mẫu (sau khi seed)

| Username | Password | Role |
|---|---|---|
| `admin01` | `Password@123` | Ban điều hành (`admin`) |
| `manager01` | `Password@123` | Quản lý kho (`warehouse_manager`) |
| `keeper01` | `Password@123` | Thủ kho (`warehouse_keeper`) |

---

## Cấu trúc thư mục

```
warehouse-ai-system/
├── backend/
│   ├── app/
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── supplier.py
│   │   │   ├── category.py
│   │   │   ├── goods.py
│   │   │   ├── purchase_order.py
│   │   │   ├── goods_receipt.py
│   │   │   ├── goods_issue.py
│   │   │   ├── stocktake.py
│   │   │   ├── supplier_invoice.py
│   │   │   ├── supplier_offer.py    # Bảng chào giá của NCC
│   │   │   ├── buyer_request.py     # Đặt mua từ khách hàng
│   │   │   └── ai_interaction_log.py
│   │   ├── routers/             # Router từng nghiệp vụ
│   │   │   ├── goods.py
│   │   │   ├── suppliers.py
│   │   │   ├── purchase_orders.py
│   │   │   ├── goods_receipts.py
│   │   │   ├── goods_issues.py
│   │   │   ├── stocktakes.py
│   │   │   ├── supplier_invoices.py
│   │   │   ├── reports.py
│   │   │   ├── ai_features.py
│   │   │   ├── supplier_portal.py   # Cổng NCC
│   │   │   ├── buyer_portal.py      # Cổng khách hàng
│   │   │   ├── categories.py
│   │   │   └── users.py
│   │   ├── auth/                # JWT + phân quyền
│   │   ├── ai/                  # Tích hợp Gemini API
│   │   │   ├── prompts/         # Tách prompt ra file riêng
│   │   │   ├── inventory_report_service.py
│   │   │   ├── reorder_suggestion_service.py
│   │   │   └── scheduler.py     # Chạy ngầm kiểm tra tồn kho
│   │   ├── schemas/             # Marshmallow validate
│   │   ├── extensions.py        # db, jwt, ma instances
│   │   └── main.py              # Application factory
│   ├── instance/
│   │   └── warehouse.db         # SQLite DB (tự tạo khi chạy lần đầu)
│   ├── scripts/
│   │   ├── seed_docker.sh       # Script seed dùng trong Docker
│   │   └── generate_seed_hash.py
│   ├── tests/                   # 14 file test pytest
│   ├── seed_database.py         # Script seed dữ liệu mẫu
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── package.json          # Lệnh chạy static server port 5500
│   ├── index.html               # Trang đăng nhập
│   ├── dashboard.html           # Dashboard tổng quan
│   ├── supplier-portal.html     # Cổng nhà cung cấp
│   ├── buyer-portal.html        # Cổng khách hàng
│   ├── vendor-login.html        # Đăng nhập NCC
│   ├── pages/
│   │   ├── goods.html
│   │   ├── suppliers.html
│   │   ├── purchase-orders.html
│   │   ├── goods-receipts.html
│   │   ├── goods-issues.html
│   │   ├── stocktakes.html
│   │   ├── invoices.html
│   │   ├── reports.html
│   │   └── ai-features.html
│   ├── css/
│   ├── js/
│   ├── Dockerfile               # Nginx:alpine, serve static + proxy /api
│   └── nginx.conf               # Reverse proxy /api → backend:5000
├── database/
│   └── seed_data.sql
├── docs/
│   ├── api_contract.md
│   ├── ai_prompt_log.md
│   └── test_report.md
└── docker-compose.yml           # Gộp backend + frontend
```

---

## API nhanh (curl)

```bash
# Đăng nhập
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin01","password":"Password@123"}'

# Lấy thông tin user (thay <token> bằng token từ bước trên)
curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer <token>"

# AI: Báo cáo tồn kho
curl -X POST http://localhost:5000/api/ai/inventory-report \
  -H "Authorization: Bearer <token>"

# AI: Gợi ý nhập hàng
curl -X POST http://localhost:5000/api/ai/reorder-suggestion \
  -H "Authorization: Bearer <token>"
```

---

## 🐳 Triển khai bằng Docker (Khuyến nghị)

> Yêu cầu: [Docker Desktop](https://www.docker.com/products/docker-desktop/) đã được cài đặt.

### Bước 1 — Tạo file `.env`

```bash
cd backend
cp .env.example .env
# Mở .env và điền các giá trị thật:
#   SECRET_KEY=<chuỗi ngẫu nhiên dài>
#   GEMINI_API_KEY=<key Gemini của bạn>
```

### Bước 2 — Build và chạy toàn hệ thống

```bash
# Chạy từ thư mục warehouse-ai-system/
docker compose up --build
```

Sau khi khởi động xong:

| Dịch vụ | Địa chỉ |
|---|---|
| **Frontend (Giao diện web)** | http://localhost |
| **API Backend trực tiếp** | http://localhost:5000/api/... |

### Bước 3 — Seed dữ liệu mẫu (lần đầu)

```bash
docker exec warehouse-backend sh /app/scripts/seed_docker.sh
```

### Bước 4 — Dừng hệ thống

```bash
docker compose down          # Dừng, giữ lại dữ liệu DB
docker compose down -v       # Dừng VÀ xóa DB (reset hoàn toàn)
```

### Cấu trúc Docker

```
warehouse-ai-system/
├── backend/
│   ├── Dockerfile           # Python:3.11-slim, chạy Flask
│   └── .dockerignore
├── frontend/
│   ├── Dockerfile           # Nginx:alpine, serve static + proxy /api
│   ├── nginx.conf           # Reverse proxy /api → backend:5000
│   └── .dockerignore
└── docker-compose.yml       # Gộp 2 services + volume SQLite
```

> **Lưu ý bảo mật**: File `backend/.env` chứa API key và SECRET_KEY thật — **không bao giờ commit** lên Git.
