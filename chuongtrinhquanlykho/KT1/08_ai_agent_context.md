# 8. Bộ context cho AI Agent

## 8.1. Mục đích

Bộ context này giúp AI Agent hiểu đúng phạm vi hệ thống quản lý kho khi hỗ trợ viết báo cáo, thiết kế hoặc review. Đây là hồ sơ tài liệu độc lập; không yêu cầu thay đổi source code hiện có.

## 8.2. Nguồn sự thật

1. Yêu cầu nghiệp vụ trong `de_tai_07.md`.
2. Quy tắc làm việc trong `AGENTS.md`.
3. Thiết kế và quy ước trong thư mục `KT1`.
4. Hợp đồng API và code hiện tại chỉ dùng để đối chiếu khi cần.

## 8.3. Nguyên tắc cho Agent

- Ưu tiên nghiệp vụ nhập, xuất, kiểm kê và tồn kho chính xác.
- Không tự bịa số liệu, bảng, API hoặc vai trò chưa có trong đặc tả.
- Không để AI tự tạo phiếu hoặc tự cập nhật tồn.
- Mọi đề xuất AI phải kèm câu: “Gợi ý từ AI chỉ mang tính tham khảo, không tự động tạo phiếu nhập/xuất kho.”
- Khi mô tả database, phải nêu transaction và điều kiện không âm.
- Khi có khác biệt giữa tài liệu và code, phải ghi rõ khác biệt thay vì âm thầm sửa code.
- Tài liệu báo cáo dùng actor Quản trị viên, Thủ kho, Kế toán; role kỹ thuật hiện tại được ghi ở phần ánh xạ.

## 8.4. Prompt khung

**System:** Bạn là chuyên gia phân tích hệ thống quản lý kho. Chỉ sử dụng dữ liệu được cung cấp. Không tự tạo số liệu hoặc nghiệp vụ. Hãy nêu giả định nếu thông tin chưa đủ.

**User:** Dựa trên tài liệu KT1, hãy [phân tích quy trình / mô tả ERD / viết user story / kiểm tra wireframe]. Kết quả phải chỉ ra actor, dữ liệu vào, dữ liệu ra, điều kiện lỗi và quy tắc không cho tồn kho âm.

## 8.5. Checklist đầu ra

- Có mục tiêu và phạm vi.
- Có actor và quyền hạn.
- Có luồng chính và luồng ngoại lệ.
- Có dữ liệu vào/ra.
- Có ràng buộc tồn kho.
- Có giới hạn của AI.
- Không yêu cầu sửa code nếu người dùng chỉ cần tài liệu báo cáo.
