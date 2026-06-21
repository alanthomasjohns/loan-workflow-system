from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.loan_document import (
    LoanDocument,
    ProcessingStatus
)

from app.services.pdf_service import (
    extract_text_from_pdf
)


@celery_app.task
def process_document(document_id: int):

    db = SessionLocal()
    try:

        document = (db.query(LoanDocument).filter(LoanDocument.id == document_id).first())
        if not document:
            return

        document.processing_status = ProcessingStatus.PROCESSING
        db.commit()
        extracted_text = extract_text_from_pdf(document.file_path)
        document.extracted_text = extracted_text

        document.processing_status = ProcessingStatus.COMPLETED
        db.commit()

        return {
            "document_id": document_id,
            "status": "completed"
        }

    except Exception as e:
        if document:
            document.processing_status = ProcessingStatus.FAILED
            db.commit()
        raise e

    finally:
        db.close()