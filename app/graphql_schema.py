import strawberry
from typing import List, Optional
from strawberry.types import Info
from sqlalchemy.orm import Session

from app.database import get_db
from app import services, models



@strawberry.type
class TenantType:
    id: str
    name: str


@strawberry.type
class InvoiceType:
    id: str
    tenant_id: str
    amount: float
    currency: str
    status: str


@strawberry.type
class MatchType:
    id: str
    invoice_id: str
    bank_transaction_id: str
    score: float
    status: str



def get_db_from_context(info: Info) -> Session:
    return info.context["db"]



@strawberry.type
class Query:

    @strawberry.field
    def tenants(self, info: Info) -> List[TenantType]:
        db = get_db_from_context(info)
        return db.query(models.Tenant).all()

    @strawberry.field
    def invoices(
        self,
        info: Info,
        tenant_id: str,
        status: Optional[str] = None,
    ) -> List[InvoiceType]:
        db = get_db_from_context(info)

        filters = {}
        if status:
            filters["status"] = status

        return services.list_invoices(db, tenant_id, filters)



@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_tenant(self, info: Info, name: str) -> TenantType:
        db = get_db_from_context(info)
        return services.create_tenant(db, name)

    @strawberry.mutation
    def create_invoice(
        self,
        info: Info,
        tenant_id: str,
        amount: float
    ) -> InvoiceType:
        db = get_db_from_context(info)
        return services.create_invoice(db, tenant_id, {"amount": amount})

    @strawberry.mutation
    def confirm_match(
        self,
        info: Info,
        tenant_id: str,
        match_id: str
    ) -> MatchType:
        db = get_db_from_context(info)
        return services.confirm_match(db, tenant_id, match_id)



schema = strawberry.Schema(query=Query, mutation=Mutation)
