# Hệ thống quản lý kho

Mã nguồn project nằm trong thư mục [`chuongtrinhquanlykho/warehouse-ai-system`](chuongtrinhquanlykho/warehouse-ai-system/).

Đọc [README hướng dẫn chạy project](chuongtrinhquanlykho/warehouse-ai-system/README.md) để biết cách khởi động:

- Backend Flask/Python tại port `5000`.
- Frontend HTML/JS + Bootstrap tại port `5500`.
- Docker Compose cho toàn hệ thống tại port `80`.

## Giao diện đăng nhập

Khi chạy frontend local bằng port `5500`:

- [http://127.0.0.1:5000](http://localhost:5500/index.html) — Đăng nhập nhân viên
- [http://localhost:5500/vendor-login.html](http://localhost:5500/vendor-login.html) — Đăng nhập nhà cung cấp
- [http://localhost:5500/buyer-portal.html](http://localhost:5500/buyer-portal.html) — Cổng gửi yêu cầu mua hàng (không cần đăng nhập)

Khi chạy bằng Docker Compose/Nginx (port `80`):

- [http://localhost/index.html](http://localhost/index.html) — Đăng nhập nhân viên
- [http://localhost/vendor-login.html](http://localhost/vendor-login.html) — Đăng nhập nhà cung cấp
- [http://localhost/buyer-portal.html](http://localhost/buyer-portal.html) — Cổng gửi yêu cầu mua hàng (không cần đăng nhập)