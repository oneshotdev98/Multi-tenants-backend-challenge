from fastapi import FastAPI, Depends, Header, Body, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import SessionLocal

from app.database import Base, engine, get_db
from app import models
from app.ai import explain
from app.reconciliation import score_match
import app.graphql_schema as graphql_schema

from strawberry.fastapi import GraphQLRouter

from app.schemas import (
    TenantCreate,
    TenantResponse,
    InvoiceCreate,
    InvoiceResponse,
    InvoiceFilters,
    BankTransactionImport,
    BankTransactionResponse,
    MatchResponse,
    AIExplanationResponse,
)

from app.services import (
    create_tenant,
    create_invoice,
    list_invoices,
    delete_invoice,
    import_transactions,
    reconcile,
    confirm_match,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Tenant Invoice Reconciliation API")

# graphql_app = GraphQLRouter(
#     graphql_schema.schema,
#     context_getter=lambda request: {"db": next(get_db())},
# )

def get_context():
    db = SessionLocal()
    try:
        yield {"db": db}
    finally:
        db.close()


graphql_app = GraphQLRouter(
    graphql_schema.schema,
    context_getter=get_context
)

app.include_router(graphql_app, prefix="/graphql")




@app.post("/tenants", response_model=TenantResponse)
def create_tenant_endpoint(
    payload: TenantCreate,
    db: Session = Depends(get_db),
):
    return create_tenant(db, payload.name)



@app.post(
    "/tenants/{tenant_id}/invoices",
    response_model=InvoiceResponse,
)
def create_invoice_endpoint(
    tenant_id: str,
    payload: InvoiceCreate,
    db: Session = Depends(get_db),
):
    return create_invoice(db, tenant_id, payload.model_dump())


@app.get(
    "/tenants/{tenant_id}/invoices",
    response_model=List[InvoiceResponse],
)
def list_invoices_endpoint(
    tenant_id: str,
    status: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(
            status_code=400,
            detail="min_amount cannot be greater than max_amount",
        )

    filters = {
        "status": status,
        "min_amount": min_amount,
        "max_amount": max_amount,
    }
    return list_invoices(db, tenant_id, filters)


@app.delete("/tenants/{tenant_id}/invoices/{invoice_id}")
def delete_invoice_endpoint(
    tenant_id: str,
    invoice_id: str,
    db: Session = Depends(get_db),
):
    delete_invoice(db, tenant_id, invoice_id)
    return {"deleted": True}



@app.post(
    "/tenants/{tenant_id}/bank-transactions/import",
    response_model=List[BankTransactionResponse],
)
def import_bank_endpoint(
    tenant_id: str,
    payload: List[BankTransactionImport] = Body(...),
    idempotency_key: str = Header(...),
    db: Session = Depends(get_db),
):
    return import_transactions(
        db,
        tenant_id,
        [tx.model_dump() for tx in payload],
        idempotency_key,
    )



@app.post(
    "/tenants/{tenant_id}/reconcile",
    response_model=List[MatchResponse],
)
def reconcile_endpoint(
    tenant_id: str,
    db: Session = Depends(get_db),
):
    return reconcile(db, tenant_id)


@app.post(
    "/tenants/{tenant_id}/matches/{match_id}/confirm",
    response_model=MatchResponse,
)
def confirm_match_endpoint(
    tenant_id: str,
    match_id: str,
    db: Session = Depends(get_db),
):
    return confirm_match(db, tenant_id, match_id)



@app.get(
    "/tenants/{tenant_id}/reconcile/explain",
    response_model=AIExplanationResponse,
)
def explain_endpoint(
    tenant_id: str,
    invoice_id: str,
    transaction_id: str,
    db: Session = Depends(get_db),
):
    invoice = db.query(models.Invoice).filter_by(
        id=invoice_id,
        tenant_id=tenant_id
    ).first()

    transaction = db.query(models.BankTransaction).filter_by(
        id=transaction_id,
        tenant_id=tenant_id
    ).first()

    if not invoice or not transaction:
        raise HTTPException(status_code=404, detail="Invoice or transaction not found")

    score = score_match(invoice, transaction)

    return {
        "explanation": explain(invoice, transaction, score)
    }


@app.get("/")
def health_check():
    return {"health status": "ok"}

