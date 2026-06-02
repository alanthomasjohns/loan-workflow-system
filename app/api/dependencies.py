from app.core.database import SessionLocal
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import decode_access_token

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

def get_current_user(access_token: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    payload = decode_access_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    public_id = payload.get("sub")
    if not public_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.id == public_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user