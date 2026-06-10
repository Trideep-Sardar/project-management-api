from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserUpdate, UserResponse
from app.models import User
from app.dependencies import get_current_user, require_role
from app.database import get_db
from app.services import get_user_by_id, get_all_users, update_user
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])


# routes related to current user
@router.get("/me", response_model=UserResponse)
def get_me_router(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me_router(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_user(current_user.id, user_data, db)


# routes specific to user id
@router.get("/{user_id}", response_model=UserResponse)
def get_user_router(
    user_id: UUID,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db),
):
    return get_user_by_id(user_id, db)


@router.put("/{user_id}", response_model=UserResponse)
def update_user_router(
    user_id: UUID,
    user_data: UserUpdate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db),
):
    return update_user(user_id, user_data, db)


@router.get("/", response_model=list[UserResponse])
def get_users_router(
    current_user: User = Depends(require_role(["admin"])), db: Session = Depends(get_db)
):
    return get_all_users(db)
