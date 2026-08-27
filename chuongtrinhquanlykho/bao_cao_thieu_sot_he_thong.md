# Báo Cáo Rà Soát Hệ Thống Quản Lý Kho (Thiếu sót và Cần hoàn thiện)

**Cập nhật ngày 27/08/2026:**
- ✅ Frontend + Backend đã kết nối thành công
- ✅ Hệ thống đăng nhập hoạt động (JWT auth)
- ✅ Dashboard load được với dữ liệu seed (8 mặt hàng, 4 dưới ngưỡng Min)
- ✅ Phân quyền theo role: admin, warehouse_manager, warehouse_keeper

**Seed data test accounts:**
- `admin01` / `Password@123` → Ban điều hành
- `manager01` / `Password@123` → Quản lý kho
- `keeper01` / `Password@123` → Thủ kho

---

Mình đã rà hệ thống. Backend có **120 test pass**, nhưng vẫn thiếu các phần quan trọng sau:

## Thiếu chức năng nghiệp vụ

1. **Quản lý tài khoản người dùng**
   - Có model `User` và đăng nhập, nhưng chưa có API CRUD user, khóa/mở tài khoản, đổi role.
   - Đặc tả yêu cầu chỉ Admin được quản lý tài khoản.

2. **Audit log hệ thống**
   - Chưa có bảng/model/API ghi lại thao tác tạo, hủy phiếu, thanh toán, duyệt kiểm kê.
   - Hiện chỉ có `ai_interaction_logs`, không thay thế được audit log nghiệp vụ.

3. **Sao lưu và phục hồi database**
   - Chưa có script backup/restore định kỳ hoặc thủ công.
   - Đây là yêu cầu phi chức năng bắt buộc trong `Prompt.md`.

4. **Thông báo scheduler**
   - Scheduler chỉ gọi AI và ghi log; chưa gửi thông báo cho thủ kho/quản lý qua email, notification hoặc giao diện.
   - Chưa có lịch sử các cảnh báo tồn kho.

5. **Thanh lý hàng hỏng/hết hạn**
   - Stocktake có trường `action`, nhưng chưa có quy trình/API riêng: thủ kho đề xuất, quản lý phê duyệt, cập nhật trạng thái thanh lý.

6. **Quản lý danh mục**
   - Có bảng `categories`, nhưng không có endpoint CRUD hoặc giao diện quản lý danh mục.

7. **Đối chiếu PO với phiếu nhập**
   - Có kiểm tra PO thuộc đúng nhà cung cấp, nhưng chưa thấy xử lý đầy đủ số lượng đặt so với số lượng thực nhận, cũng như cảnh báo khi nhận lệch PO.

## Thiếu về kỹ thuật

- Thư mục schema gần như rỗng, chỉ có placeholder: `__init__.py:1`. Dữ liệu đang được validate thủ công trong từng router.
- `AI_PROVIDER` được khai báo nhưng code thực tế chỉ gọi Gemini: `inventory_report_service.py:7`.
- AI báo cáo tồn kho hiện chỉ gửi dữ liệu từ `goods`, chưa tổng hợp lịch sử nhập/xuất như đặc tả yêu cầu: `ai_features.py:20`.
- Chưa có cơ chế chia nhỏ dữ liệu khi nhiều SKU, có nguy cơ vượt giới hạn token.
- API AI trả lỗi 500 kèm nội dung exception thô, có thể làm lộ chi tiết dịch vụ bên ngoài.
- CORS đang mở toàn bộ origin: `main.py:71`.
- Có secret mặc định không an toàn nếu quên cấu hình `.env`: `main.py:99`.
- Thiếu dependency `marshmallow-sqlalchemy`, gây warning khi chạy test.
- Có nhiều cảnh báo deprecated từ `Query.get()` và `datetime.utcnow()`.

## Thiếu tài liệu bàn giao

Theo đặc tả, hiện còn thiếu:
- `phan_tich_thiet_ke.md`
- `erd.mmd` và ảnh ERD
- `use_case.md`
- `final_report.md`
- Báo cáo test đầy đủ cho toàn bộ module (File `test_report.md:1` mới cập nhật chi tiết chủ yếu cho Reports; các module Auth và phần lớn test AI vẫn ghi “Chưa chạy”).

## Ưu tiên nên làm trước

**Đã hoàn thành:**
- ✅ Frontend + Backend integration (serve frontend files, CORS, static routes)
- ✅ Đăng nhập và JWT auth hoạt động
- ✅ Seed data script với 3 test users
- ✅ Database path consistency (instance/warehouse.db)

**Cần làm tiếp:**
1. Audit log và quản lý tài khoản (CRUD user, khóa/mở tài khoản).
2. Backup/restore database.
3. Hoàn thiện đối chiếu PO, thanh lý hàng và thông báo scheduler.
4. Thêm schema validation, xử lý lỗi AI và giới hạn dữ liệu AI.
5. Hoàn thiện tài liệu/báo cáo bàn giao (ERD, design, use case, final report).
6. Kiểm tra phân quyền trên tất cả endpoints theo role.
7. Test toàn bộ flow từ login → CRUD data → AI features → báo cáo.
