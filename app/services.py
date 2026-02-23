import hashlib
import json
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import models
from app.reconciliation import score_match


def _serialize_bank_tx(tx: models.BankTransaction):
    return {
        "id": tx.id,
        "tenant_id": tx.tenant_id,
        "external_id": tx.external_id,
        "amount": tx.amount,
        "currency": tx.currency,
        "description": tx.description,
        "posted_at": tx.posted_at.isoformat() if tx.posted_at else None,
        "created_at": tx.created_at.isoformat() if tx.created_at else None,
    }


def _get_tenant_or_404(db: Session, tenant_id: str):
    tenant = db.query(models.Tenant).filter_by(id=tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


def create_tenant(db: Session, name: str):
    tenant = models.Tenant(name=name)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


def create_invoice(db: Session, tenant_id: str, data):
    _get_tenant_or_404(db, tenant_id)

    invoice = models.Invoice(tenant_id=tenant_id, **data)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice


def list_invoices(db: Session, tenant_id: str, filters, skip=0, limit=20):
    _get_tenant_or_404(db, tenant_id)
    query = db.query(models.Invoice).filter_by(tenant_id=tenant_id)

    if filters.get("status"):
        query = query.filter(models.Invoice.status == filters["status"])

    if filters.get("min_amount"):
        query = query.filter(models.Invoice.amount >= filters["min_amount"])

    if filters.get("max_amount"):
        query = query.filter(models.Invoice.amount <= filters["max_amount"])

    return query.offset(skip).limit(limit).all()


def delete_invoice(db: Session, tenant_id: str, invoice_id: str):
    _get_tenant_or_404(db, tenant_id)

    invoice = db.query(models.Invoice).filter_by(
        id=invoice_id,
        tenant_id=tenant_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found for tenant")

    db.delete(invoice)
    db.commit()


def import_transactions(db: Session, tenant_id: str, txs, key: str):
    _get_tenant_or_404(db, tenant_id)

    if not key or not key.strip():
        raise HTTPException(status_code=400, detail="Idempotency key is required")

    if not txs:
        raise HTTPException(status_code=400, detail="At least one transaction is required")

    payload_hash = hashlib.sha256(
        json.dumps(
            txs,
            sort_keys=True,
            default=lambda value: value.isoformat() if hasattr(value, "isoformat") else str(value),
        ).encode()
    ).hexdigest()

    existing = db.query(models.IdempotencyKey).filter_by(
        tenant_id=tenant_id,
        key=key
    ).first()

    if existing:
        if existing.payload_hash != payload_hash:
            raise HTTPException(status_code=409, detail="Idempotency conflict")
        return json.loads(existing.response)

    created = []
    for tx in txs:
        obj = models.BankTransaction(tenant_id=tenant_id, **tx)
        db.add(obj)
        created.append(obj)

    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Duplicate bank transaction for tenant/external_id",
        )

    response_payload = [_serialize_bank_tx(tx) for tx in created]

    record = models.IdempotencyKey(
        tenant_id=tenant_id,
        key=key,
        payload_hash=payload_hash,
        response=json.dumps(response_payload),
    )

    db.add(record)
    db.commit()

    return response_payload


def reconcile(db: Session, tenant_id: str):
    _get_tenant_or_404(db, tenant_id)

    invoices = db.query(models.Invoice).filter_by(tenant_id=tenant_id).all()
    transactions = db.query(models.BankTransaction).filter_by(tenant_id=tenant_id).all()

    if not invoices:
        raise HTTPException(status_code=404, detail="No invoices found for tenant")

    if not transactions:
        raise HTTPException(status_code=404, detail="No bank transactions found for tenant")

    results = []

    for inv in invoices:
        for tx in transactions:
            s = score_match(inv, tx)
            if s > 0:
                match = models.Match(
                    tenant_id=tenant_id,
                    invoice_id=inv.id,
                    bank_transaction_id=tx.id,
                    score=s,
                )
                db.add(match)
                results.append(match)

    db.commit()

    return results


def confirm_match(db: Session, tenant_id: str, match_id: str):
    _get_tenant_or_404(db, tenant_id)

    match = db.query(models.Match).filter_by(
        id=match_id,
        tenant_id=tenant_id
    ).first()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found for tenant")

    if match.status == "confirmed":
        raise HTTPException(status_code=409, detail="Match is already confirmed")

    match.status = "confirmed"

    invoice = db.query(models.Invoice).filter_by(
        id=match.invoice_id,
        tenant_id=tenant_id
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice for match not found")

    invoice.status = "matched"

    db.commit()
    db.refresh(match)

    return match
