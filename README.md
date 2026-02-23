# Multi-Tenant Invoice Reconciliation API

FastAPI backend for tenant-scoped invoice reconciliation with deterministic scoring, idempotent bank imports, and optional AI explanation output.

## What This Project Delivers

- Tenant creation and scoped data access
- Invoice CRUD (create, list with filters, delete)
- Bank transaction import with idempotency protection
- Reconciliation match generation with weighted heuristic scoring
- Match confirmation flow
- AI explanation endpoint for a candidate pair
- REST + GraphQL access

## Tech Stack

- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy 2.x
- Pydantic Settings
- Strawberry GraphQL
- LangChain + Google Gemini (for explanation text)
- PostgreSQL (recommended), SQLite supported for tests

## Project Layout

- `app/main.py`: FastAPI app and routes
- `app/models.py`: SQLAlchemy models and DB constraints
- `app/services.py`: business logic and HTTP-level validation/errors
- `app/reconciliation.py`: deterministic scoring function
- `app/ai.py`: LLM explanation chain + fallback behavior
- `app/graphql_schema.py`: GraphQL schema/resolvers
- `tests/`: pytest suite for API and service behavior

## Setup and Run

1. Create a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Configure environment.

Create `.env` (or copy from `.env.example`) with:

```env
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:<port>/<db>
GOOGLE_API_KEY=<your_google_api_key>
```

4. Run the server.

```bash
uvicorn app.main:app --reload
```

5. Open:

- Swagger: `http://127.0.0.1:8000/docs`
- Graphql: `http://127.0.0.1:8000/graphql`
- Health: `GET /`

## API Summary

- `POST /tenants`
- `POST /tenants/{tenant_id}/invoices`
- `GET /tenants/{tenant_id}/invoices?status=&min_amount=&max_amount=`
- `DELETE /tenants/{tenant_id}/invoices/{invoice_id}`
- `POST /tenants/{tenant_id}/bank-transactions/import` (`Idempotency-Key` header required)
- `POST /tenants/{tenant_id}/reconcile`
- `POST /tenants/{tenant_id}/matches/{match_id}/confirm`
- `GET /tenants/{tenant_id}/reconcile/explain?invoice_id=...&transaction_id=...`

All entity IDs are UUID strings.

## Reconciliation Scoring (Deterministic)

Defined in `app/reconciliation.py`:

- amount exact match: `+50`
- amount near match (`abs(diff) <= 5`): `+20`
- date proximity (`<= 3` days): `+20`
- description containment: `+10`

Final score is additive. Pairs with `score > 0` become `proposed` matches.

## Idempotency Strategy

Implemented in `app/services.py` (`import_transactions`):

- Require `Idempotency-Key`
- Hash request payload deterministically (sorted JSON, datetime-safe serialization)
- If `(tenant_id, key)` exists:
  - same hash: return stored response
  - different hash: return `409 Idempotency conflict`
- If key not found:
  - persist transactions
  - persist idempotency record with response payload

This enables safe retries without creating duplicates.

## Key Design Decisions and Tradeoffs

- Service-layer orchestration keeps route handlers thin and maintainable.
- Multi-tenancy is enforced through explicit `tenant_id` filtering in service operations.
- Error handling is explicit and consistent (`400`, `404`, `409`) for predictable API behavior.
- UUID identifiers improve external safety and avoid guessable IDs.
- `Base.metadata.create_all(...)` is used for simplicity; no migration framework is included.

Tradeoffs:

- Reconcile currently evaluates all invoice/transaction combinations for a tenant.
- No background jobs or async queue for heavy reconciliation workloads.
- No Alembic migrations yet, so schema evolution is manual.

## Tests (Run Locally)

Run:

```bash
pytest -q
```

Current suite covers:

- invoice creation flow
- bank import success + idempotent replay + idempotency conflict
- reconcile success + missing prerequisite behavior
- confirm match success + duplicate confirm conflict
- AI explanation endpoint response

## Manual End-to-End Test Flow

1. `POST /tenants`
2. `POST /tenants/{tenant_id}/invoices`
3. `POST /tenants/{tenant_id}/bank-transactions/import` (with `Idempotency-Key`)
4. `POST /tenants/{tenant_id}/reconcile`
5. `POST /tenants/{tenant_id}/matches/{match_id}/confirm`
6. `GET /tenants/{tenant_id}/reconcile/explain?...`


