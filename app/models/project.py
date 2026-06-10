from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import Relationship
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

# project members table has only 2 foreign keys for link so directly defining table instead of class
project_members = Table(
    "project_members",
    Base.metadata,
    Column("project_id", UUID(as_uuid=True), ForeignKey("projects.id")),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
)


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="active")
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # RelationShips
    members = Relationship("User", secondary=project_members)
    owner = Relationship("User", back_populates="owned_projects")
    tasks = Relationship("Task", back_populates="project")
