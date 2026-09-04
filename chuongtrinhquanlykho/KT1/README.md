# Hồ sơ KT1 - Phân tích yêu cầu và thiết kế hệ thống

Bộ tài liệu này phục vụ riêng cho báo cáo Giai đoạn 1 (Bài KT1). Nội dung không thay đổi mã nguồn hiện có trong `warehouse-ai-system`.

## Thành phần

- `03_phan_tich_thiet_ke.md`: phát biểu yêu cầu, quy trình và kiến trúc mức khái niệm.
- `04_erd.mmd`: sơ đồ ERD Mermaid.
- `04_erd.svg`: ảnh sơ đồ ERD để chèn vào báo cáo.
- `05_actor_use_case.md`: actor, quyền hạn và đặc tả use case.
- `06_wireframe.md`: mô tả wireframe và liên kết các ảnh minh họa.
- `06_wireframe_dashboard.svg`: wireframe dashboard tồn kho.
- `06_wireframe_goods_receipt.svg`: wireframe phiếu nhập kho.
- `06_wireframe_goods_issue.svg`: wireframe phiếu xuất kho.
- `08_ai_agent_context.md`: bộ context và nguyên tắc dùng AI Agent trong KT1.
- `claude.md`, `codebase-map.md`, `architecture.md`, `user-stories.md`: các tệp context độc lập cho agent.

## Quy ước phạm vi

- Đây là tài liệu thiết kế và báo cáo, không phải bản thay thế source code.
- Actor theo đề bài gồm Quản trị viên, Thủ kho và Kế toán. Hệ thống hiện tại có thêm tên role kỹ thuật `warehouse_manager`; tài liệu ánh xạ vai trò này vào nhóm nghiệp vụ quản lý kho/kế toán để không làm thay đổi code.
- ERD thể hiện thiết kế logic; các ràng buộc tồn kho âm được trình bày bằng văn bản vì Mermaid ERD không biểu diễn đầy đủ transaction và constraint.
