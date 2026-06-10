from app.schemas import UserCreate, Token
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def register_user(user: UserCreate, db: Session) -> User:
    logger.info(f"Register Attempt : {user.email}")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )
    new_user = User(
        name=user.name, email=user.email, hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User registered successfully : {user.email}")
    return new_user


def login_user(db: Session, email: str, password: str) -> Token:
    logger.info(f"Login attempt : {email}")
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user or not verify_password(
        password, existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    token = create_access_token({"sub": email})
    logger.info(f"User logged in : {email}")
    return token
