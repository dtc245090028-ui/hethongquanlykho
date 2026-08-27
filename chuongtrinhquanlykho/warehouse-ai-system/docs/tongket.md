# TỔNG KẾT GIAI ĐOẠN 1
## Phân tích yêu cầu và thiết kế hệ thống (Bài KT1)

**Đề tài:** Hệ thống quản lý kho có tích hợp AI  
**Ngày tổng kết:** 27/08/2026  
**Phạm vi đánh giá:** Giai đoạn 1 trong `de_tai_07.md`, đối chiếu với đặc tả, tài liệu, backend, frontend và test hiện có.

---

## Slide 1. Mục tiêu của Giai đoạn 1

Giai đoạn 1 yêu cầu sử dụng AI để hỗ trợ:

1. Phân tích quy trình nhập kho, xuất kho, kiểm kê và báo cáo tồn.
2. Thiết kế ERD và ràng buộc để tránh tồn kho âm.
3. Xác định actor và quyền hạn của từng actor.
4. Đề xuất chức năng AI sinh báo cáo và gợi ý nhập hàng.
5. Sinh wireframe cho phiếu nhập, phiếu xuất và dashboard tồn kho.

---

## Slide 2. Kết luận tổng quát

### Kết luận: CHƯA HOÀN THÀNH 100%

Giai đoạn 1 đã hoàn thành phần **phân tích nền tảng và thiết kế khung hệ thống**, đồng thời nhiều thiết kế đã được triển khai thành code để kiểm chứng.

Tuy nhiên, chưa thể kết luận hoàn thành đầy đủ vì:

- Chưa có bộ tài liệu KT1 riêng gồm phân tích thiết kế, ERD, use case và wireframe được đóng gói rõ ràng.
- ERD hiện nằm trong `Prompt.md` dưới dạng Mermaid, chưa có file `erd.mmd` riêng và chưa có ảnh sơ đồ.
- Danh sách actor trong các tài liệu chưa hoàn toàn thống nhất với role thực tế trong hệ thống.
- Wireframe chưa được lưu thành tài liệu hoặc hình ảnh wireframe riêng; hiện chủ yếu thể hiện qua giao diện HTML đã xây dựng.
- Một số yêu cầu thiết kế trong đặc tả rộng hơn phần đã triển khai thực tế.

**Mức đánh giá đề xuất:** Đạt nền tảng KT1, nhưng cần hoàn thiện hồ sơ và thống nhất đặc tả trước khi xem là hoàn tất.

---

## Slide 3. Đánh giá yêu cầu 1: Phân tích quy trình kho

### Trạng thái: ĐẠT CƠ BẢN

Đã xác định được các quy trình chính:

- Tạo đơn đặt hàng với nhà cung cấp.
- Nhận hàng và lập phiếu nhập kho.
- Cập nhật tồn kho khi nhập hàng.
- Lập phiếu xuất và kiểm tra tồn trước khi xuất.
- Kiểm kê, tính chênh lệch và xử lý theo luồng đề xuất/phê duyệt.
- Theo dõi hóa đơn và thanh toán nhà cung cấp.
- Tổng hợp báo cáo và cảnh báo tồn kho.

### Cơ sở đối chiếu

- `Prompt.md` mục 3.3 đến 3.7 mô tả nghiệp vụ kho.
- `Prompt.md` mục 7.3 mô tả luồng dữ liệu chính.
- Backend đã có các model/router tương ứng cho PO, nhập, xuất, kiểm kê, hóa đơn và báo cáo.
- Các test nghiệp vụ nhập, xuất, kiểm kê và báo cáo đã được xây dựng.

### Điểm còn thiếu

- Chưa có sơ đồ quy trình riêng để đưa trực tiếp vào slide.
- Một số quy trình mở rộng trong đặc tả chưa hoàn thiện trong hệ thống, như audit log, thanh lý hàng hỏng và thông báo scheduler.

---

## Slide 4. Đánh giá yêu cầu 2: Thiết kế ERD

### Trạng thái: ĐẠT VỀ NỘI DUNG, CHƯA ĐẠT VỀ HỒ SƠ BÀN GIAO

Thiết kế dữ liệu đã xác định đầy đủ các nhóm bảng chính:

- Người dùng, nhà cung cấp, danh mục và hàng hóa.
- Đơn đặt hàng và chi tiết đơn đặt hàng.
- Phiếu nhập và chi tiết phiếu nhập.
- Phiếu xuất và chi tiết phiếu xuất.
- Phiếu kiểm kê và chi tiết kiểm kê.
- Hóa đơn nhà cung cấp và thanh toán.
- Nhật ký tương tác AI.

Các quan hệ chính đã được mô tả trong Mermaid ở `Prompt.md` mục 6.2.

### Ràng buộc quan trọng đã xác định

- `goods.quantity_on_hand` chỉ thay đổi qua giao dịch nhập, xuất hoặc kiểm kê.
- Không cho xuất vượt số lượng tồn hiện có.
- `goods_receipt_items.unit_price` lưu giá nhập theo từng lần nhập.
- Kiểm kê phải đi theo luồng: Thủ kho đề xuất, Quản lý kho phê duyệt, sau đó mới cập nhật tồn.
- Các bảng chi tiết liên kết với bảng nghiệp vụ bằng khóa ngoại.

### Điểm chưa hoàn tất

- Chưa tách ERD thành file `docs/erd.mmd`.
- Chưa có ảnh ERD để chèn vào PowerPoint.
- Chưa thể hiện đầy đủ các ràng buộc nghiệp vụ trên một sơ đồ hoặc tài liệu thiết kế riêng.

---

## Slide 5. Đánh giá yêu cầu 3: Actor và phân quyền

### Trạng thái: ĐẠT MỘT PHẦN, CẦN THỐNG NHẤT

Đặc tả đã nhận diện các actor:

- Ban điều hành/Admin.
- Quản lý kho.
- Thủ kho.
- Nhà cung cấp, là actor gián tiếp.
- Scheduler của hệ thống.

Trong code hiện có ba role đăng nhập:

- `admin`.
- `warehouse_manager`.
- `warehouse_keeper`.

Phân quyền backend đã được áp dụng ở cấp route bằng decorator `roles_required`, không chỉ ẩn nút trên giao diện.

### Điểm chưa thống nhất

- `de_tai_07.md` ban đầu nhắc đến actor kế toán, nhưng hệ thống thực tế dùng `warehouse_manager` và chưa có role kế toán riêng.
- Một số tài liệu gọi Admin là Ban điều hành, trong khi code dùng tên role `admin`.
- Nhà cung cấp và Scheduler được mô tả là actor nhưng không có tài khoản đăng nhập trực tiếp.

### Kết luận

Mô hình actor hiện đủ để chạy MVP, nhưng cần thống nhất cách gọi actor, role và quyền hạn trong báo cáo cuối kỳ.

---

## Slide 6. Đánh giá yêu cầu 4: Chức năng AI

### Trạng thái: ĐẠT CƠ BẢN

Đã đề xuất và triển khai hai chức năng AI chính:

1. **Báo cáo tình trạng kho**
   - Phân tích tồn kho hiện tại.
   - Trả về tóm tắt tình hình.
   - Liệt kê hàng dưới ngưỡng.
   - Ghi nhận biến động đáng chú ý.

2. **Gợi ý nhập hàng**
   - Dựa trên tồn kho hiện tại.
   - Dựa trên mức tồn tối thiểu.
   - Dựa trên tổng số lượng xuất trong 30 ngày gần nhất.

Ngoài ra, hệ thống đã có:

- Prompt template tách riêng trong `backend/app/ai/prompts/`.
- Model `AIInteractionLog` để lưu lịch sử gọi AI.
- Scheduler quét hàng dưới ngưỡng.
- Test mock Gemini cho hai endpoint AI.

### Điểm chưa hoàn tất

- Báo cáo tồn kho hiện chủ yếu gửi snapshot từ bảng `goods`, chưa tổng hợp đầy đủ lịch sử nhập/xuất như thiết kế trong `Prompt.md` mục 8.1.
- `AI_PROVIDER` mới được khai báo nhưng service thực tế vẫn phụ thuộc Gemini.
- Scheduler mới ghi log và chưa gửi thông báo thật cho người dùng.
- Cần cấu hình model Gemini hợp lệ trong `.env` khi demo thực tế.

---

## Slide 7. Đánh giá yêu cầu 5: Wireframe và giao diện dự kiến

### Trạng thái: ĐẠT VỀ GIAO DIỆN, CHƯA ĐỦ HỒ SƠ WIREFRAME

Frontend đã có các màn hình tương ứng với thiết kế nghiệp vụ:

- Đăng nhập.
- Dashboard tồn kho.
- Hàng hóa.
- Nhà cung cấp.
- Đơn đặt hàng.
- Phiếu nhập kho.
- Phiếu xuất kho.
- Kiểm kê kho.
- Hóa đơn và công nợ.
- Báo cáo.
- AI Trợ lý.

Dashboard đã thể hiện các nhóm thông tin chính như:

- Tổng số hàng hóa.
- Hàng dưới ngưỡng.
- Phiếu nhập gần nhất.
- Phiếu xuất gần nhất.
- Đơn đặt hàng đang xử lý.

### Điểm chưa hoàn tất

- Chưa có file wireframe riêng ở dạng ảnh, Figma, Draw.io hoặc tài liệu mô tả bố cục.
- Giao diện hiện tại là prototype/ứng dụng HTML đã triển khai, chưa có phần thuyết minh quyết định thiết kế giao diện.

---

## Slide 8. Những phần đã hoàn thành có thể trình bày

- Phân tích được bài toán quản lý kho và các nghiệp vụ cốt lõi.
- Xác định được các bảng dữ liệu và quan hệ chính.
- Xác định được luồng cập nhật tồn kho an toàn.
- Xác định được actor và phân quyền cơ bản.
- Xác định được hai chức năng AI phù hợp với bài toán.
- Xây dựng được prototype giao diện cho các màn hình chính.
- Có backend, database, frontend và test để kiểm chứng thiết kế.
- Có nhật ký sử dụng AI trong `docs/ai_prompt_log.md`.

---

## Slide 9. Những phần cần bổ sung để hoàn tất Giai đoạn 1

Các việc cần hoàn thiện ở mức tài liệu, ưu tiên theo thứ tự:

1. Tạo `docs/phan_tich_thiet_ke.md` mô tả bài toán, luồng nghiệp vụ và quyết định thiết kế.
2. Tách sơ đồ Mermaid thành `docs/erd.mmd`.
3. Xuất ảnh ERD để chèn vào báo cáo/PowerPoint.
4. Tạo `docs/use_case.md` với actor, use case và phân quyền thống nhất.
5. Tạo tài liệu hoặc ảnh wireframe cho dashboard, phiếu nhập và phiếu xuất.
6. Thống nhất việc gọi actor kế toán, quản lý kho và Admin giữa `de_tai_07.md`, `Prompt.md` và code.
7. Ghi rõ giới hạn hiện tại của chức năng AI trong báo cáo.
8. Cập nhật nhật ký AI cho các lần dùng AI để phân tích, thiết kế và review.

---

## Slide 10. Kết luận dùng khi thuyết trình

> Giai đoạn 1 đã hoàn thành phần phân tích yêu cầu và xây dựng thiết kế nền tảng cho hệ thống quản lý kho tích hợp AI. Nhóm đã xác định được quy trình nghiệp vụ, mô hình dữ liệu, actor, phân quyền và hai chức năng AI chính. Thiết kế đã được kiểm chứng bằng backend, frontend và các test nghiệp vụ.
>
> Tuy nhiên, Giai đoạn 1 chưa hoàn tất 100% về mặt hồ sơ vì còn thiếu các tài liệu tách riêng như ERD, use case, phân tích thiết kế và wireframe. Ngoài ra, cần thống nhất lại actor kế toán với role quản lý kho trong đặc tả. Vì vậy, trạng thái phù hợp là **đạt nền tảng KT1, cần hoàn thiện tài liệu để hoàn tất**.

---

## Phụ lục. Bằng chứng đối chiếu

| Nội dung | Bằng chứng hiện có |
|---|---|
| Đặc tả mục tiêu và nghiệp vụ | `de_tai_07.md`, `Prompt.md` |
| Actor, use case, ERD và luồng dữ liệu | `Prompt.md` mục 5, 6, 7.3 |
| Model và quan hệ database | `backend/app/models/` |
| API nghiệp vụ | `backend/app/routers/`, `docs/api_contract.md` |
| Giao diện và prototype wireframe | `frontend/`, đặc biệt `dashboard.html` và `pages/` |
| Chức năng AI | `backend/app/ai/`, `backend/app/routers/ai_features.py` |
| Nhật ký dùng AI | `docs/ai_prompt_log.md`, `docs/log_entry.md` |
| Kiểm thử | `backend/tests/`, `docs/test_report.md` |
| Các thiếu sót đã ghi nhận | `bao_cao_thieu_sot_he_thong.md`, `docs/doi_chieu_bao_cao_va_phien_1.md` |
