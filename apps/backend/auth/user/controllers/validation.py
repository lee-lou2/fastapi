from sqlalchemy.orm import Session

from ..models import User


def get_by_email(db: Session, email: str):
    user = db.query(User).filter_by(email=email).first()
    return user and user.user_local
