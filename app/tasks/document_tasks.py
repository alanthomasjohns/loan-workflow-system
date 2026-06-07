from app.core.celery_app import celery_app


@celery_app.task
def process_document(document_id: int):
    print(f"Processing document {document_id}")

    return {"document_id": document_id, "status": "processed"}