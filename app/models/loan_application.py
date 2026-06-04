from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    Enum,
)

from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import (
    TimestampMixin,
    SoftDeleteMixin,
    PublicUUIDMixin,
)

from app.models.enums import (
    LoanStatus,
    EmploymentType,
)

class LoanApplication(Base, PublicUUIDMixin, TimestampMixin, SoftDeleteMixin,):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    term_months = Column(Integer, nullable=False)
    annual_income = Column(Numeric(12, 2), nullable=False)
    employment_type = Column(Enum(EmploymentType), nullable=False)
    status = Column(Enum(LoanStatus), default=LoanStatus.PENDING, nullable=False)
    documents = relationship("LoanDocument", back_populates="loan_application")

    user = relationship("User", back_populates="loan_applications")