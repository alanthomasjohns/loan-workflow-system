from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    get_current_user,
)

from app.models.loan_application import LoanApplication
from app.models.user import User

from app.schemas.loan import (
    LoanApplicationCreate,
    LoanApplicationResponse,
)


router = APIRouter(prefix="/loans", tags=["Loans"],)


@router.post("", response_model=LoanApplicationResponse,)
def create_loan(payload: LoanApplicationCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user),):
    loan = LoanApplication(
        user_id=current_user.id,
        amount=payload.amount,
        term_months=payload.term_months,
        annual_income=payload.annual_income,
        employment_type=payload.employment_type,
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan