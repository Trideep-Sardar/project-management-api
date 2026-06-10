from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas import CommentCreate, CommentResponse
from app.models import Comment, User
from uuid import UUID


def create_comment(
    data: CommentCreate, current_user_id: UUID, task_id: UUID, db: Session
) -> Comment:
    new_comment = Comment(
        content=data.content, task_id=task_id, author_id=current_user_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comment_by_id(task_id: UUID, comment_id: UUID, db: Session) -> Comment:
    existing_comment = (
        db.query(Comment)
        .filter(
            Comment.id == comment_id,
            Comment.task_id == task_id,
        )
        .first()
    )
    if not existing_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return existing_comment


def get_all_comments(task_id: UUID, db: Session) -> list[Comment]:
    return db.query(Comment).filter(Comment.task_id == task_id).all()


def delete_comment(
    task_id: UUID, current_user: User, comment_id: UUID, db: Session
) -> dict:
    existing_comment = get_comment_by_id(task_id, comment_id, db)
    if existing_comment.author_id == current_user.id or current_user.role == "admin":
        pass
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment",
        )
    db.delete(existing_comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
