from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: UUID
    content: str
    task_id: UUID
    author_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
