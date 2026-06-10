from fastapi import APIRouter, Depends
from app.services import login_user, register_user
from sqlalchemy.orm import Session
from app.schemas import UserResponse, UserCreate, Token
from app.models import User
from app.dependencies import get_current_user
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register_user_router(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


@router.post("/login", response_model=Token)
def login_user_router(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    token = login_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}
