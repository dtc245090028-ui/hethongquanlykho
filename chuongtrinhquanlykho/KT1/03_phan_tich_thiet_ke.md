# 3. Phân tích yêu cầu và thiết kế hệ thống

## 3.1. Phát biểu bài toán

Doanh nghiệp nhỏ cần quản lý hàng hóa, nhà cung cấp, nhập kho, xuất kho, kiểm kê và tồn kho. Cách quản lý bằng bảng tính dễ phát sinh sai lệch, khó truy vết giao dịch và không phát hiện sớm hàng sắp hết. Hệ thống được xây dựng để số hóa nghiệp vụ kho, bảo đảm tồn kho nhất quán và hỗ trợ AI tạo báo cáo, nhận xét biến động và gợi ý nhập hàng.

## 3.2. Mục tiêu

1. Quản lý tập trung hàng hóa, danh mục, nhà cung cấp và người dùng.
2. Lập phiếu nhập, phiếu xuất và cập nhật tồn kho có kiểm soát.
3. Kiểm kê, ghi nhận chênh lệch và phê duyệt trước khi điều chỉnh tồn.
4. Cung cấp báo cáo nhập - xuất - tồn và cảnh báo dưới mức tối thiểu.
5. Dùng AI để tóm tắt số liệu và đề xuất nhập hàng, nhưng không cho AI tự thay đổi dữ liệu.

## 3.3. Yêu cầu chức năng

| Mã | Yêu cầu |
|---|---|
| FR-01 | Đăng nhập và phân quyền theo vai trò. |
| FR-02 | Quản lý hàng hóa, danh mục, đơn vị tính và mức tồn tối thiểu/tối đa. |
| FR-03 | Quản lý nhà cung cấp. |
| FR-04 | Lập phiếu nhập, kiểm tra dữ liệu và tăng tồn trong transaction. |
| FR-05 | Lập phiếu xuất, kiểm tra tồn và không cho xuất vượt số lượng hiện có. |
| FR-06 | Lập phiếu kiểm kê, ghi nhận số thực tế và chênh lệch. |
| FR-07 | Phê duyệt chênh lệch kiểm kê trước khi cập nhật tồn. |
| FR-08 | Tra cứu lịch sử nhập/xuất theo hàng hóa, thời gian và nhà cung cấp. |
| FR-09 | Hiển thị cảnh báo hàng dưới tồn tối thiểu. |
| FR-10 | Tổng hợp báo cáo nhập - xuất - tồn. |
| FR-11 | AI sinh báo cáo tóm tắt và gợi ý nhập hàng từ dữ liệu được cung cấp. |

## 3.4. Yêu cầu phi chức năng

- **Toàn vẹn:** cập nhật tồn phải nằm trong transaction; không cho `quantity_on_hand < 0`.
- **Truy vết:** mọi chứng từ giữ người tạo, thời gian và chi tiết hàng hóa.
- **Bảo mật:** mật khẩu được băm; phân quyền kiểm tra ở backend.
- **Khả dụng:** nghiệp vụ nhập, xuất, kiểm kê và báo cáo số liệu gốc vẫn chạy khi AI không hoạt động.
- **Dễ dùng:** lỗi và xác nhận nghiệp vụ hiển thị bằng tiếng Việt.

## 3.5. Quy trình nghiệp vụ

### Nhập kho

1. Thủ kho chọn nhà cung cấp và, nếu có, đơn đặt hàng.
2. Nhập danh sách hàng, số lượng thực nhận và đơn giá của lần nhập.
3. Hệ thống kiểm tra dữ liệu và đối chiếu số lượng đặt/thực nhận.
4. Trong một transaction, lưu phiếu nhập, chi tiết phiếu và cộng tồn.
5. Hệ thống trả mã phiếu và tồn mới.

### Xuất kho

1. Thủ kho nhập mục đích xuất và danh sách hàng.
2. Hệ thống đọc tồn hiện tại.
3. Nếu có dòng vượt tồn, từ chối toàn bộ giao dịch.
4. Nếu hợp lệ, trong một transaction lưu phiếu xuất và trừ tồn.
5. Hệ thống trả mã phiếu và số lượng tồn sau xuất.

### Kiểm kê

1. Thủ kho tạo kỳ kiểm kê và nhập số lượng thực tế.
2. Hệ thống lấy số hệ thống, tính `difference = actual_quantity - system_quantity`.
3. Thủ kho đề xuất cách xử lý chênh lệch.
4. Quản trị viên hoặc người được phân quyền phê duyệt/từ chối.
5. Chỉ phiếu đã phê duyệt mới được điều chỉnh tồn và lưu lịch sử trước/sau.

### Báo cáo tồn

1. Người dùng chọn kỳ báo cáo.
2. Hệ thống tổng hợp tồn đầu kỳ, nhập, xuất, điều chỉnh và tồn cuối kỳ.
3. Hệ thống đánh dấu hàng dưới Min, hàng tồn lâu và biến động lớn.
4. Người có quyền xem báo cáo số liệu; AI chỉ nhận phần dữ liệu cần phân tích.

## 3.6. Thiết kế AI

- **Báo cáo AI:** tóm tắt tình trạng tồn, hàng dưới Min và biến động đáng chú ý.
- **Gợi ý nhập hàng:** dựa trên tồn hiện tại, Min/Max và tốc độ xuất trong kỳ.
- **Nguyên tắc:** AI chỉ phân tích input; không tự tạo số liệu, không tự tạo phiếu và không tự cập nhật tồn.
- **Fallback:** nếu AI lỗi, vẫn hiển thị báo cáo số liệu gốc và thông báo dịch vụ AI tạm thời không khả dụng.

## 3.7. Ràng buộc dữ liệu cốt lõi

1. Khóa ngoại phải bật giữa bảng nghiệp vụ và bảng chi tiết.
2. Số lượng giao dịch phải là số dương.
3. `goods.quantity_on_hand` chỉ thay đổi qua nhập, xuất hoặc kiểm kê đã duyệt.
4. Trước khi trừ tồn phải kiểm tra `quantity_requested <= quantity_on_hand` trong cùng transaction.
5. `goods_receipt_items.unit_price` là giá của lần nhập, không lấy lại từ giá hiện tại.
6. Không xóa chứng từ đã phát sinh giao dịch nếu việc xóa làm mất lịch sử; dùng trạng thái hủy khi cần.

## 3.8. Kiến trúc mức khái niệm

Người dùng thao tác trên giao diện web. Frontend gọi backend API. Backend kiểm tra xác thực, phân quyền và nghiệp vụ; sau đó dùng ORM/transaction để ghi SQLite hoặc PostgreSQL. Lớp AI nhận dữ liệu đã tổng hợp, gọi model bên ngoài và lưu log tương tác. AI là lớp hỗ trợ, không nằm trên đường đi bắt buộc của nghiệp vụ kho.
