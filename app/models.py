from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, UniqueConstraint, Index
from datetime import datetime, timezone
from uuid import uuid4
from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    invoice_date = Column(DateTime)
    description = Column(Text)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_invoice_tenant_status", "tenant_id", "status"),
    )


class BankTransaction(Base):
    __tablename__ = "bank_transactions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False, index=True)
    external_id = Column(String)
    posted_at = Column(DateTime)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("tenant_id", "external_id", name="uq_tenant_external"),
    )


class Match(Base):
    __tablename__ = "matches"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    invoice_id = Column(String(36), nullable=False)
    bank_transaction_id = Column(String(36), nullable=False)
    score = Column(Float)
    status = Column(String, default="proposed")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id = Column(String(36), nullable=False)
    key = Column(String, nullable=False)
    payload_hash = Column(String, nullable=False)
    response = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("tenant_id", "key", name="uq_tenant_key"),
    )
