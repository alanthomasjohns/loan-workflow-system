from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.models.enums import (
    DocumentType,
    DocumentStatus,
)


class DocumentResponse(BaseModel):
    public_id: UUID
    document_type: DocumentType
    original_file_name: str
    content_type: str
    file_size: int
    status: DocumentStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }