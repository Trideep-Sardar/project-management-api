from app.models import User
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserUpdate
from uuid import UUID
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def get_user_by_id(user_id: UUID, db: Session) -> User:
    logger.info(f"Accessing user : {user_id}")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    logger.info("User accessed successfully")
    return db_user


def get_all_users(db: Session) -> list[User]:
    logger.info("Accessing all users")
    return db.query(User).all()


def update_user(user_id: UUID, user: UserUpdate, db: Session) -> User:
    logger.info(f"Updating user data : {user_id}")
    user_data = user.model_dump(exclude_unset=True)
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    for key, value in user_data.items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)
    logger.info(f"User data updated successfully : {user_id}")
    return existing_user
