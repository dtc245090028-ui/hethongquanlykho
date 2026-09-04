# 5. Actor và đặc tả User Story / Use Case

## 5.1. Actor

| Actor | Trách nhiệm |
|---|---|
| Quản trị viên | Quản lý tài khoản, phân quyền, cấu hình hệ thống, xem báo cáo tổng hợp và quản lý dữ liệu nền. |
| Thủ kho | Quản lý hàng hóa thực tế, lập phiếu nhập/xuất, kiểm kê và đề xuất xử lý chênh lệch. |
| Kế toán | Theo dõi chứng từ nhập/xuất, hóa đơn, công nợ và báo cáo nhập - xuất - tồn. |
| Nhà cung cấp | Actor gián tiếp: cung cấp hàng, báo giá và xác nhận đơn đặt hàng. |
| Scheduler hệ thống | Quét hàng dưới Min và kích hoạt tác vụ AI định kỳ. |

**Ánh xạ với code hiện tại:** `admin` tương ứng Quản trị viên; `warehouse_keeper` tương ứng Thủ kho; `warehouse_manager` đang đảm nhiệm nhóm quyền quản lý kho và một phần nghiệp vụ Kế toán. Đây là quy ước của hồ sơ báo cáo, không yêu cầu sửa role trong source code.

## 5.2. Danh sách use case

| Mã | Use case | Actor chính |
|---|---|---|
| UC-01 | Đăng nhập và phân quyền | Tất cả người dùng |
| UC-02 | Quản lý hàng hóa/danh mục | Quản trị viên, Thủ kho |
| UC-03 | Quản lý nhà cung cấp | Quản trị viên, Thủ kho |
| UC-04 | Lập phiếu nhập kho | Thủ kho |
| UC-05 | Lập phiếu xuất kho | Thủ kho |
| UC-06 | Kiểm kê và xử lý chênh lệch | Thủ kho, Quản trị viên |
| UC-07 | Theo dõi hóa đơn và công nợ | Kế toán |
| UC-08 | Xem báo cáo nhập - xuất - tồn | Kế toán, Quản trị viên |
| UC-09 | Nhận cảnh báo dưới tồn tối thiểu | Thủ kho, Kế toán |
| UC-10 | Sinh báo cáo AI | Kế toán, Quản trị viên |
| UC-11 | Gợi ý nhập hàng bằng AI | Thủ kho, Kế toán |

## 5.3. User story

### US-01: Nhập kho

Là Thủ kho, tôi muốn lập phiếu nhập với số lượng thực nhận và đơn giá từng lần nhập để tồn kho được cộng chính xác và có thể truy vết.

**Tiêu chí nghiệm thu:** không lưu số lượng âm/0; phiếu hợp lệ làm tăng tồn trong transaction; lưu được người lập và thời gian.

### US-02: Xuất kho không âm

Là Thủ kho, tôi muốn hệ thống kiểm tra tồn trước khi xuất để không thể xuất vượt số lượng hiện có.

**Tiêu chí nghiệm thu:** nếu một dòng vượt tồn thì toàn bộ phiếu bị từ chối; tồn không thay đổi; trả lỗi tiếng Việt rõ ràng.

### US-03: Kiểm kê có phê duyệt

Là Thủ kho, tôi muốn nhập số đếm thực tế và đề xuất xử lý chênh lệch; người có quyền phê duyệt sẽ quyết định trước khi tồn được điều chỉnh.

**Tiêu chí nghiệm thu:** phiếu chờ duyệt không làm đổi tồn; phiếu đã duyệt lưu chênh lệch và tồn trước/sau.

### US-04: Báo cáo tồn kho

Là Kế toán, tôi muốn xem nhập - xuất - tồn theo kỳ để đối chiếu chứng từ và lập báo cáo.

**Tiêu chí nghiệm thu:** báo cáo có kỳ, tồn đầu, nhập, xuất, điều chỉnh, tồn cuối và danh sách dưới Min.

### US-05: Trợ lý AI

Là Kế toán hoặc Thủ kho, tôi muốn AI tóm tắt biến động và gợi ý nhập hàng dựa trên số liệu thật để hỗ trợ quyết định.

**Tiêu chí nghiệm thu:** input có nguồn từ dữ liệu tổng hợp; output không được tự thêm số liệu; luôn hiển thị cảnh báo AI chỉ mang tính tham khảo.
