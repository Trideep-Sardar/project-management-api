from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "active"


class MembersInfo(BaseModel):
    id: UUID
    name: str
    email: str

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    status: str
    owner_id: UUID
    created_at: datetime
    members: list[MembersInfo]

    class Config:
        from_attributes = True
