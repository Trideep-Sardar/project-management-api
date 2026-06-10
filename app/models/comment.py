from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Relationship
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships

    task = Relationship("Task", back_populates="comments")
    author = Relationship("User", back_populates="comments")
