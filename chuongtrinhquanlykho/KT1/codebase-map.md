# Codebase Map

## Root

- `warehouse-ai-system/`: ứng dụng quản lý kho hiện có.
- `KT1/`: hồ sơ phân tích, thiết kế và context phục vụ báo cáo.

## Application

- `warehouse-ai-system/backend/app/main.py`: Flask application factory và đăng ký router.
- `warehouse-ai-system/backend/app/models/`: model SQLAlchemy.
- `warehouse-ai-system/backend/app/routers/`: API nghiệp vụ.
- `warehouse-ai-system/backend/app/ai/`: service, prompt và scheduler AI.
- `warehouse-ai-system/backend/tests/`: test backend.
- `warehouse-ai-system/frontend/`: HTML, JavaScript và CSS giao diện.
- `warehouse-ai-system/database/seed_data.sql`: dữ liệu mẫu.
- `warehouse-ai-system/docs/api_contract.md`: hợp đồng API.

## KT1 documents

- `03_phan_tich_thiet_ke.md`: requirements and workflows.
- `04_erd.mmd`: logical database diagram.
- `05_actor_use_case.md`: actors and user stories.
- `06_wireframe.md`: wireframe descriptions.
- `08_ai_agent_context.md`: agent rules and prompt frame.
