# 6. Wireframe màn hình

Các ảnh SVG trong thư mục này là wireframe mức bố cục, dùng để chèn vào báo cáo. Chúng không thay thế giao diện triển khai.

## 6.1. Dashboard tồn kho

Ảnh: [06_wireframe_dashboard.svg](06_wireframe_dashboard.svg)

Bố cục gồm thanh điều hướng, bộ lọc kỳ báo cáo, bốn chỉ số nhanh, biểu đồ nhập/xuất, bảng hàng dưới Min và hoạt động gần đây. Mục tiêu là giúp Kế toán và Quản trị viên nắm tình trạng kho trong một màn hình.

## 6.2. Phiếu nhập kho

Ảnh: [06_wireframe_goods_receipt.svg](06_wireframe_goods_receipt.svg)

Bố cục gồm thông tin nhà cung cấp, số PO, ngày nhận, ghi chú, bảng mặt hàng với số lượng và đơn giá, tổng tiền, nút lưu/hủy. Khi lưu, hệ thống phải xác thực và cập nhật tồn bằng transaction.

## 6.3. Phiếu xuất kho

Ảnh: [06_wireframe_goods_issue.svg](06_wireframe_goods_issue.svg)

Bố cục gồm ngày xuất, mục đích/bộ phận nhận, bảng mặt hàng, cột tồn hiện tại, số lượng xuất và cảnh báo tồn. Nút lưu chỉ được thực hiện khi mọi dòng không vượt tồn.

## 6.4. Nguyên tắc giao diện

- Hiển thị rõ trạng thái chứng từ: nháp, đã ghi nhận, chờ duyệt, đã duyệt, đã hủy.
- Hiển thị tồn hiện tại ngay cạnh ô số lượng nhập/xuất.
- Cảnh báo lỗi tại dòng dữ liệu gây lỗi.
- Có xác nhận trước thao tác hủy.
