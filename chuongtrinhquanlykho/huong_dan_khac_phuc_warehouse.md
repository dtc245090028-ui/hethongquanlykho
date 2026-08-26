Đúng, nên ưu tiên **chạy được và nghiệp vụ đúng trước**, còn bảo mật nâng cao và độ khớp tuyệt đối với Prompt có thể để sau.

Hiện trạng thực tế:

- Backend **biên dịch được**.
- Toàn bộ test hiện tại **120 test pass**.
- Lỗi đăng nhập hiện tại chủ yếu do **seed sai file database**, không phải do JWT hay logic đăng nhập.

**Việc cần xử lý ngay**

1. **Seed đúng database backend đang dùng**

Backend đang dùng:

```text
backend/app/instance/warehouse.db
```

Chạy từ thư mục `warehouse-ai-system/backend`:

```powershell
Get-Content ..\database\seed_data.sql -Raw |
  sqlite3 .\app\instance\warehouse.db
```

Kiểm tra:

```powershell
sqlite3 .\app\instance\warehouse.db "SELECT username, role FROM users;"
```

2. **Đảm bảo backend và frontend đang chạy đúng port**

Backend:

```powershell
cd warehouse-ai-system/backend
python -m app.main
```

Frontend, mở terminal khác:

```powershell
cd warehouse-ai-system/frontend
python -m http.server 8000
```

Truy cập:

```text
http://localhost:8000
```

Frontend hiện đã gọi API đến:

```text
http://localhost:5000/api
```

3. **Không dùng nhầm các file database khác**

Các file sau đang dễ gây nhầm:

```text
warehouse-ai-system/warehouse.db
warehouse-ai-system/backend/warehouse.db
warehouse-ai-system/backend/instance/warehouse.db
warehouse-ai-system/backend/app/instance/warehouse.db
```

Khi chạy Python trực tiếp, chỉ nên kiểm tra và seed file:

```text
backend/app/instance/warehouse.db
```

**Các lỗi nghiệp vụ nên ưu tiên sau khi đăng nhập chạy được**

- Nhập/xuất số lượng sai có thể trả lỗi `500` thay vì lỗi rõ ràng `400`.
- Tạo hàng hóa với `category_id` hoặc `supplier_id` không tồn tại có thể gây lỗi database.
- Kiểm kê có khả năng ghi đè tồn kho nếu trong lúc chờ duyệt đã phát sinh nhập/xuất.
- Một số API danh sách chưa giới hạn `page_size`, có thể làm giao diện hoặc truy vấn chậm.
- Docker seed hiện chưa chắc chạy được vì image backend không chứa `database/seed_data.sql`.

**Có thể tạm bỏ qua lúc này**

- Secret JWT mặc định.
- CORS mở rộng.
- Migration Alembic.
- Gunicorn.
- Audit log.
- Backup/restore.
- Hỗ trợ nhiều AI provider.
- Các cảnh báo deprecated.
- Chuẩn hóa toàn bộ schema theo Prompt.

Tóm lại: **chưa cần sửa toàn bộ backend ngay**. Bước đầu tiên là seed đúng `backend/app/instance/warehouse.db`, đăng nhập kiểm tra ba tài khoản mẫu, sau đó kiểm tra từng luồng nhập, xuất, kiểm kê và hóa đơn. Chỉ khi một luồng thực sự lỗi mới sửa code ở luồng đó.