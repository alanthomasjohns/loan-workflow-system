from sqlalchemy import Column, Integer, String, ForeignKey,Enum, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.mixins import (
    PublicUUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
)
from app.models.enums import DocumentType, DocumentStatus, ProcessingStatus


class LoanDocument(Base, PublicUUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "loan_documents"

    id = Column(Integer, primary_key=True, index=True)
    loan_application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    original_file_name = Column(String(255), nullable=False)
    stored_file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING, nullable=False)
    processing_status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    extracted_text = Column(Text, nullable=True)

    loan_application = relationship("LoanApplication", back_populates="documents")