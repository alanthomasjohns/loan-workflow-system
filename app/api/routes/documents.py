from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.loan_application import LoanApplication
from app.models.loan_document import LoanDocument
from app.models.enums import DocumentType
from app.schemas.document import DocumentResponse
from app.core.constants import ALLOWED_DOCUMENT_TYPES, MAX_DOCUMENT_SIZE


router = APIRouter(prefix="/documents", tags=["Documents"],)

@router.post("/{loan_public_id}", response_model=DocumentResponse,)
async def upload_document(
        loan_public_id: str,
        document_type: DocumentType = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
    loan = db.query(LoanApplication).filter(LoanApplication.public_id == loan_public_id).first()

    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )
    if loan.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed",
        )

    if file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type",
        )

    contents = await file.read()
    if len(contents) > MAX_DOCUMENT_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large",
        )

    extension = Path(file.filename).suffix

    stored_file_name = (f"{uuid4()}{extension}")
    upload_dir = Path("uploads")

    upload_dir.mkdir(parents=True, exist_ok=True,)
    file_path = (upload_dir / stored_file_name)
    with open(file_path, "wb") as f:
        f.write(contents)

    document = LoanDocument(
        loan_application_id=loan.id,
        document_type=document_type,
        original_file_name=file.filename,
        stored_file_name=stored_file_name,
        file_path=str(file_path),
        content_type=file.content_type,
        file_size=len(contents),
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document