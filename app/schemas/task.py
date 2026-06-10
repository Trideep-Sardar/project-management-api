from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"
    priority: str = "medium"


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assigned_to: UUID | None = None


class AssignedUser(BaseModel):
    id: UUID
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    status: str
    priority: str
    assigned_user: AssignedUser | None = None
    project_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TaskPaginatedResponse(BaseModel):
    data: list[TaskResponse]
    total: int
    total_pages: int
    page: int
    limit: int
    has_next: bool
    has_prev: bool
