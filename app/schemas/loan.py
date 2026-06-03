from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import (
    EmploymentType,
    LoanStatus,
)


class LoanApplicationCreate(BaseModel):
    amount: Decimal
    term_months: int
    annual_income: Decimal
    employment_type: EmploymentType


class LoanApplicationResponse(BaseModel):
    public_id: UUID

    amount: Decimal
    term_months: int
    annual_income: Decimal
    employment_type: EmploymentType
    status: LoanStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }