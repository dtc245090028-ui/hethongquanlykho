<!-- ppt-master-schema: design-spec/v1 -->
# Warehouse AI Phase 1 Presentation - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | Warehouse AI Phase 1 Presentation |
| Canvas Format | PPT 16:9 (1280 x 720) |
| Page Count | 10 |
| Primary Language | vi-VN |
| Target Audience | Giảng viên và nhóm dự án CNTT |
| Communication Intent | Báo cáo tiến độ KT1, giải thích nền tảng đã xây dựng, nêu rõ bằng chứng và khoảng trống cần hoàn thiện |
| Desired Audience Outcome | Người nghe hiểu hệ thống đã đạt nền tảng nhưng chưa hoàn tất hồ sơ 100%, đồng thời nắm được các việc ưu tiên tiếp theo |
| Core Message / Ask / Action | Công nhận nền tảng KT1 đã đạt; thống nhất hoàn thiện hồ sơ ERD, use case, phân tích thiết kế và wireframe để đóng giai đoạn |
| Delivery Context | Trình bày trực tiếp, có người thuyết trình; tệp cũng đủ rõ để xem lại sau buổi trình bày |
| Artifact Afterlife | Review, đánh giá KT1 và làm hồ sơ bàn giao |
| Reading Mode | balanced |
| Content Strategy | Balanced default: cô đọng và sắp xếp lại nội dung để làm rõ tiến độ, bằng chứng và rủi ro; không thêm số liệu ngoài nguồn |
| Design Style | Báo cáo dữ liệu editorial: lưới rõ, cột thông tin, rule mảnh, khối nhấn tiết chế |
| AI Image Acquisition Path | not applicable; use native diagrams and shapes |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | disabled — user did not request notes |
| Custom Animations | disabled — user did not request animations |
| Narration Audio | disabled — user did not request narration |
| Created Date | 2026-08-27 |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 x 720 |
| viewBox | `0 0 1280 720` |
| Margins | 64 px left/right, 48 px top/bottom |
| Content Area | x=64..1216, y=48..672 |

## III. Visual Theme

### Theme Style

- **Mode**: custom
- **Visual style**: custom
- **Theme**: Báo cáo dữ liệu editorial, dùng lưới, đường dẫn và nhãn trạng thái để biến hồ sơ kỹ thuật thành câu chuyện dễ quét
- **Tone**: Chính xác, thẳng thắn, có tính kiểm chứng và hướng hành động
- **Mode Behavior**: Mở bằng kết luận, sau đó lần lượt chứng minh qua quy trình, dữ liệu, actor, AI và giao diện; kết thúc bằng gap và backlog ưu tiên.
- **Visual Style Behavior**: Nền sáng, chữ mực đậm, khối phẳng có viền mảnh, cột editorial và nhịp rule ngang; dùng xanh ngọc cho phần đạt, cam san hô cho rủi ro, vàng nhạt cho việc cần bổ sung.

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #F7F5EF | Nền chính ấm, giảm chói khi chiếu |
| Secondary background | #E9EFEA | Nền phụ cho sơ đồ và nhóm thông tin |
| Primary | #12323A | Tiêu đề, số liệu chính, đường trục |
| Accent | #00A6A6 | Trạng thái đạt và đường dẫn hệ thống |
| Secondary accent | #F26B4F | Cảnh báo, gap và điểm cần quyết định |
| Body text | #263238 | Nội dung đọc trên nền sáng |

### AI Image Strategy

- **Image Rendering**: none
- **Visual**: Không sử dụng ảnh; ưu tiên sơ đồ, connector, bảng và hình khối native.
- **Mood**: Kỹ thuật, minh bạch, có thể kiểm chứng.

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | Humanist sans, compact and sturdy | Aptos Display | Aptos Display | Arial, sans-serif |
| Body | Neutral sans, high legibility | Aptos | Aptos | Arial, sans-serif |

- **Title stack**: Aptos Display, Arial, sans-serif
- **Body stack**: Aptos, Arial, sans-serif

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 24 |
| Title | 38 |
| Subtitle | 26 |
| Annotation | 16 |
| Compact body | 21 |
| Small body | 20 |
| Micro body | 19 |

## V. Layout Principles

### Deck-wide Direction

- **Hierarchy direction**: Nhìn từ số slide và tiêu đề sang một claim lớn, rồi xuống bằng chứng hoặc hành động.
- **Composition tendency**: Cột editorial bất đối xứng; một vùng chính rộng và một rail phụ cho trạng thái, nguồn hoặc quyết định.
- **Cross-page continuity**: Lặp lại số slide, rule ngang, nhãn section và cặp màu đạt/cần bổ sung; thay đổi topology theo loại bằng chứng.
- **Spacing posture**: Breathing ở slide mở/kết; dense có kiểm soát ở slide quy trình, actor và backlog.

## VI. Icon Usage Specification

- **Primary bundled library**: none

| Icon Path | Suitable Scenarios |
| --- | --- |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Layout pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline

### Part 1: Kết luận và nền tảng

#### Slide 01 - Nền tảng KT1 đã đạt, hồ sơ còn thiếu

- **Audience move**: Từ chờ một bản báo cáo tiến độ → hiểu ngay trạng thái tổng thể và lý do.
- **Layout**: Cover tối giản với claim lớn bên trái, chỉ báo trạng thái dạng thanh ở bên phải, footer ghi phạm vi và ngày.
- **Title**: Giai đoạn 1: đạt nền tảng, chưa hoàn tất hồ sơ
- **Core message**: Hệ thống quản lý kho tích hợp AI đã có nền tảng phân tích, thiết kế và code kiểm chứng; phần thiếu chủ yếu là hồ sơ bàn giao.
- **Content**: Đề tài: Hệ thống quản lý kho có tích hợp AI. Kết luận đề xuất: Đạt nền tảng KT1, cần hoàn thiện tài liệu để hoàn tất. Ngày: 27/08/2026. Phạm vi: Phân tích yêu cầu và thiết kế hệ thống.
- **Visualization**: Thanh trạng thái gồm hai phần: Nền tảng đã xây dựng / Hồ sơ cần đóng gói. Native-ready map: status_bar=yes.
- **Fact IDs**: F001, F002
- **Motion suggestion**: Reveal claim trước, sau đó hiện hai trạng thái để người nghe giữ được kết luận trong đầu.

#### Slide 02 - KT1 đã làm được gì và chưa làm được gì

- **Audience move**: Từ kết luận tổng quát → phân biệt rõ phần đạt và phần chưa đạt.
- **Layout**: Hai vùng đối trọng ngang; vùng đạt chiếm ưu thế, vùng chưa đạt dùng màu cảnh báo và checklist ngắn.
- **Title**: Bức tranh KT1 trong một trang
- **Core message**: Nền tảng kỹ thuật đã được kiểm chứng, nhưng bộ hồ sơ KT1 chưa đủ để gọi là hoàn tất 100%.
- **Content**: Đã có: phân tích nghiệp vụ, thiết kế dữ liệu, actor/quyền, hai chức năng AI, prototype giao diện, backend/database/frontend/test. Còn thiếu: tài liệu KT1 riêng, ERD tách file và ảnh, use case thống nhất, wireframe riêng, thống nhất actor và phạm vi triển khai.
- **Visualization**: Hai cột “Đạt nền tảng” và “Cần hoàn thiện”, mỗi cột có 5 dòng nhãn.
- **Fact IDs**: F003, F004
- **Motion suggestion**: Hiện cột đạt trước, cột gap sau để tạo nhịp báo cáo cân bằng.

### Part 2: Bằng chứng thiết kế

#### Slide 03 - Luồng kho đã được xác định từ đầu đến cuối

- **Audience move**: Từ biết có quy trình → thấy chuỗi nghiệp vụ liên tục và điểm kiểm soát tồn âm.
- **Layout**: Một flow ngang sáu bước, mỗi bước là nhãn ngắn nối bởi đường mảnh; callout dưới flow cho hai phần mở rộng còn thiếu.
- **Title**: Quy trình cốt lõi đã có khung vận hành
- **Core message**: Luồng nhập-xuất-kiểm kê-báo cáo được nối thành một chuỗi, với transaction là chốt an toàn của tồn kho.
- **Content**: 1. Đặt hàng NCC → 2. Nhận hàng/lập phiếu nhập → 3. Cập nhật tồn qua transaction → 4. Xuất hàng/chặn vượt tồn → 5. Kiểm kê/đề xuất/phê duyệt → 6. Báo cáo/cảnh báo. Mở rộng chưa hoàn thiện: audit log, thanh lý hàng hỏng, scheduler thông báo.
- **Visualization**: Flowchart native với điểm nhấn ở bước transaction và chặn xuất âm.
- **Fact IDs**: F005, F006
- **Motion suggestion**: Dẫn mắt theo hướng trái → phải, dừng ngắn tại hai chốt kiểm soát.

#### Slide 04 - ERD đủ nội dung, thiếu gói bàn giao

- **Audience move**: Từ thấy quy trình → hiểu dữ liệu đã bao phủ các nghiệp vụ chính nhưng chưa được đóng gói thành artifact riêng.
- **Layout**: Bên trái là ERD thu gọn theo 5 nhóm bảng; bên phải là rail “đã xác định / còn thiếu”.
- **Title**: Mô hình dữ liệu đã đủ để kiểm chứng nghiệp vụ
- **Core message**: Các nhóm bảng và quan hệ chính đã rõ; điểm thiếu nằm ở cách bàn giao và thể hiện ràng buộc.
- **Content**: Nhóm bảng: người dùng, NCC/danh mục/hàng hóa; PO/nhập; xuất; kiểm kê; hóa đơn/thanh toán; log AI. Ràng buộc: quantity_on_hand chỉ đổi qua transaction; không xuất vượt tồn; unit_price lưu theo lần nhập; kiểm kê phải được phê duyệt.
- **Visualization**: Diagram native nhóm bảng và connector, không dùng ảnh ERD.
- **Fact IDs**: F007, F008
- **Motion suggestion**: Hiện nhóm dữ liệu trước, overlay các ràng buộc như những “van” kiểm soát.

#### Slide 05 - Actor đã đủ cho MVP, tên gọi cần thống nhất

- **Audience move**: Từ mô hình dữ liệu → biết ai làm gì và nhận diện điểm lệch giữa đặc tả với code.
- **Layout**: Ba role đăng nhập ở trung tâm, actor gián tiếp ở hai bên; dải cảnh báo dưới cùng về role kế toán.
- **Title**: Phân quyền backend đã đi vào route
- **Core message**: MVP có ba role đăng nhập và phân quyền ở backend; còn một khoảng lệch thuật ngữ cần chốt trong báo cáo.
- **Content**: Admin: cấu hình, tài khoản, báo cáo tổng hợp. Quản lý kho: phê duyệt, dashboard, hiệu suất. Thủ kho: nhập, xuất, kiểm kê, PO. Actor gián tiếp: nhà cung cấp, scheduler. Code hiện có: admin, warehouse_manager, warehouse_keeper. Điểm lệch: đặc tả cũ nhắc kế toán nhưng chưa có role riêng.
- **Visualization**: Role map với đường nét khác nhau cho login và indirect actor.
- **Fact IDs**: F009, F010
- **Motion suggestion**: Hiện ba role login cùng lúc, sau đó thêm actor gián tiếp và nhãn “cần thống nhất”.

### Part 3: AI và prototype

#### Slide 06 - AI hỗ trợ quyết định, không thay nghiệp vụ lõi

- **Audience move**: Từ quyền hạn → hiểu AI đang đứng ở lớp hỗ trợ nào và giới hạn hiện tại.
- **Layout**: Hai cột chức năng AI ở trái; pipeline dữ liệu → prompt → log ở phải; footer là 3 giới hạn.
- **Title**: Hai chức năng AI đã được thiết kế và test
- **Core message**: AI tạo báo cáo và gợi ý nhập hàng từ dữ liệu kho; hệ thống quản lý vẫn phải chạy độc lập khi AI không sẵn sàng.
- **Content**: Báo cáo tình trạng kho: tồn hiện tại, hàng dưới ngưỡng, biến động. Gợi ý nhập hàng: tồn hiện tại, min stock, lượng xuất 30 ngày. Hỗ trợ: prompt template riêng, AIInteractionLog, scheduler, mock Gemini tests. Giới hạn: snapshot chưa đủ lịch sử, provider còn phụ thuộc Gemini, scheduler mới log chưa gửi thông báo thật.
- **Visualization**: Pipeline native 3 bước với hai nhánh AI.
- **Fact IDs**: F011, F012
- **Motion suggestion**: Reveal dữ liệu đầu vào trước, hai nhánh AI sau, giới hạn cuối cùng để giữ tính minh bạch.

#### Slide 07 - Prototype đã phủ các màn hình nghiệp vụ chính

- **Audience move**: Từ năng lực AI → thấy thiết kế đã được cụ thể hóa thành giao diện có thể demo.
- **Layout**: Một dashboard wireframe thu gọn ở trái; danh sách màn hình và trạng thái hồ sơ ở phải.
- **Title**: Giao diện đã là prototype, chưa là bộ wireframe bàn giao
- **Core message**: Frontend đã thể hiện các luồng chính đủ để demo; thiếu là tài liệu wireframe và thuyết minh quyết định thiết kế.
- **Content**: Màn hình: đăng nhập, dashboard, hàng hóa, NCC, PO, nhập, xuất, kiểm kê, hóa đơn/công nợ, báo cáo, AI Trợ lý. Dashboard hiển thị tổng hàng, hàng dưới ngưỡng, phiếu gần nhất, PO đang xử lý.
- **Visualization**: Mock dashboard native gồm header, metric strip, list blocks; không giả định số liệu mới.
- **Fact IDs**: F013, F014
- **Motion suggestion**: Hiện dashboard silhouette trước rồi gắn nhãn các module để chứng minh độ phủ.

### Part 4: Đóng giai đoạn

#### Slide 08 - Bằng chứng đã nằm trong code và test

- **Audience move**: Từ xem prototype → tin rằng thiết kế có thể kiểm chứng bằng artifact thực tế.
- **Layout**: Ba cột bằng chứng: backend/database, frontend, test/docs; footer nối về nguyên tắc truy vết.
- **Title**: Thiết kế không dừng ở sơ đồ
- **Core message**: KT1 có chuỗi bằng chứng từ đặc tả đến code, giao diện, test và nhật ký AI.
- **Content**: Backend: models, routers, auth, AI. Database: seed_data.sql và quan hệ. Frontend: dashboard.html và pages. Test: nhập, xuất, kiểm kê, báo cáo, auth, AI. Docs: api_contract, test_report, ai_prompt_log, log_entry.
- **Visualization**: Evidence chain gồm Source → Design → Implementation → Test → Documentation.
- **Fact IDs**: F015, F016
- **Motion suggestion**: Dẫn theo chuỗi bằng chứng từ trái sang phải, kết bằng “có thể truy vết”.

#### Slide 09 - Backlog hoàn thiện theo thứ tự ưu tiên

- **Audience move**: Từ biết thiếu gì → có thứ tự hành động cụ thể để đóng KT1.
- **Layout**: Danh sách 8 việc theo timeline 1–8, nhóm thành Hồ sơ, Thống nhất, Minh chứng AI.
- **Title**: Tám việc để chuyển “đạt nền tảng” thành “hoàn tất”
- **Core message**: Phần còn lại chủ yếu là đóng gói và thống nhất tài liệu, có thể xử lý theo một backlog rõ ràng.
- **Content**: 1 phan_tich_thiet_ke.md; 2 erd.mmd; 3 ảnh ERD; 4 use_case.md; 5 wireframe dashboard/nhập/xuất; 6 thống nhất actor; 7 ghi giới hạn AI; 8 cập nhật nhật ký AI.
- **Visualization**: Priority ladder 1–8, đánh dấu 1–5 là hồ sơ lõi.
- **Fact IDs**: F017
- **Motion suggestion**: Reveal theo thứ tự ưu tiên, dừng ở nhóm 1–5 như mốc đóng hồ sơ cốt lõi.

#### Slide 10 - Quyết định đề xuất

- **Audience move**: Từ backlog → đồng thuận trạng thái và bước tiếp theo.
- **Layout**: Một câu kết lớn ở trái; bên phải là ba ô quyết định: công nhận, hoàn thiện, thống nhất.
- **Title**: Đề xuất chốt trạng thái KT1
- **Core message**: Công nhận nền tảng KT1 đã đạt; chưa gọi là hoàn tất 100% cho tới khi bộ hồ sơ và thuật ngữ được thống nhất.
- **Content**: Đã đạt: quy trình, dữ liệu, actor, phân quyền, AI, prototype, code/test. Chưa hoàn tất: ERD/use case/phân tích/wireframe riêng và actor kế toán. Bước tiếp theo: hoàn thiện 5 artifact lõi, thống nhất role, cập nhật nhật ký AI và ghi rõ giới hạn AI.
- **Visualization**: Decision triad với trạng thái “Công nhận / Hoàn thiện / Thống nhất”.
- **Fact IDs**: F018, F019
- **Motion suggestion**: Hiện câu kết trước, ba quyết định sau như lời kêu gọi hành động.

## X. Speaker Notes Requirements

- **Generation**: disabled
