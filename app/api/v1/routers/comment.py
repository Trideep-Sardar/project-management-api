from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_all_comments,
)
from app.schemas import CommentCreate, CommentResponse
from uuid import UUID

router = APIRouter(
    prefix="/projects/{project_id}/tasks/{task_id}/comments", tags=["Comments"]
)


@router.post("/", response_model=CommentResponse)
def create_comment_router(
    data: CommentCreate,
    project_id: UUID,
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_comment(data, current_user.id, task_id, db)


@router.get("/", response_model=list[CommentResponse])
def get_comments_router(
    project_id: UUID,
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_all_comments(task_id, db)


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment_router(
    project_id: UUID,
    task_id: UUID,
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_comment_by_id(task_id, comment_id, db)


@router.delete("/{comment_id}")
def delete_comment_router(
    project_id: UUID,
    task_id: UUID,
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_comment(task_id, current_user, comment_id, db)
