# Architecture Context

## Logical layers

1. **Presentation:** HTML/JavaScript frontend for login, dashboard, goods, receipts, issues, stocktakes and reports.
2. **API:** Flask routes handle authentication, authorization, validation and response formatting.
3. **Domain/data:** SQLAlchemy models and SQLite database store master data, documents, stocktakes, invoices and AI logs.
4. **AI support:** prompt templates and services summarize prepared inventory data and produce reorder suggestions.

## Critical flow

Frontend -> authenticated API -> role check -> input validation -> database transaction -> response. AI is called only after deterministic data aggregation and never owns stock mutations.

## Data integrity

`goods.quantity_on_hand` is changed only by receipt, issue or approved stocktake. Issue transactions must reject quantities greater than current stock. Receipt item prices remain historical snapshots.

## Failure behavior

If the AI provider is unavailable, the application must continue serving core stock operations and deterministic reports. Errors returned to users should be Vietnamese and should not expose provider exceptions.
