from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="todo")  # todo | in_progress | done
    priority = Column(String, default="medium")  # low | medium | high
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # RelationShips
    project = Relationship("Project", back_populates="tasks")
    assigned_user = Relationship("User", back_populates="assigned_tasks")
    comments = Relationship("Comment", back_populates="task")
