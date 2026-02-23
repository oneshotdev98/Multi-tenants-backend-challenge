from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict


# =====================================================
# Base Config
# =====================================================

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Tenant Schemas
# =====================================================

class TenantCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class TenantResponse(ORMModel):
    id: str
    name: str
    created_at: datetime


# =====================================================
# Invoice Schemas
# =====================================================

class InvoiceCreate(BaseModel):
    amount: float = Field(..., gt=0)
    currency: Optional[str] = "USD"
    description: Optional[str] = None
    invoice_date: Optional[datetime] = None


class InvoiceResponse(ORMModel):
    id: str
    tenant_id: str
    amount: float
    currency: str
    description: Optional[str]
    invoice_date: Optional[datetime]
    status: str
    created_at: datetime


class InvoiceFilters(BaseModel):
    status: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# =====================================================
# Bank Transaction Schemas
# =====================================================

class BankTransactionImport(BaseModel):
    external_id: Optional[str] = None
    amount: float = Field(..., gt=0)
    currency: Optional[str] = "USD"
    description: Optional[str] = None
    posted_at: Optional[datetime] = None


class BankTransactionResponse(ORMModel):
    id: str
    tenant_id: str
    external_id: Optional[str]
    amount: float
    currency: str
    description: Optional[str]
    posted_at: Optional[datetime]
    created_at: datetime


# =====================================================
# Match Schemas
# =====================================================

class MatchResponse(ORMModel):
    id: str
    tenant_id: str
    invoice_id: str
    bank_transaction_id: str
    score: float
    status: str
    created_at: datetime


# =====================================================
# Reconciliation Response
# =====================================================

class ReconcileResponse(BaseModel):
    invoice_id: str
    bank_transaction_id: str
    score: float


# =====================================================
# AI Explanation Schema
# =====================================================

class AIExplanationResponse(BaseModel):
    explanation: str


# =====================================================
# Pagination Schema
# =====================================================

class PaginatedInvoices(BaseModel):
    total: int
    items: List[InvoiceResponse]
