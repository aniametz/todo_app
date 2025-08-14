from datetime import datetime, timezone
import enum
from typing import List
from sqlalchemy import DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from database import db
from data_models.todo_tag_association import TodoTagAssociation
import uuid

class Priority(str, enum.Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Todo(db.Model):
    __tablename__ = "todo"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    description: Mapped[str] = mapped_column(unique=True)
    priority: Mapped[Priority] = mapped_column(nullable=True, default=Priority.NONE)
    difficulty: Mapped[int] = mapped_column(CheckConstraint('(difficulty IS NULL) OR (difficulty >= 1 AND difficulty <= 5)'), nullable=True, default=None)
    todo_tags: Mapped[List[TodoTagAssociation]] = relationship("TodoTagAssociation", back_populates="todo", cascade="all, delete-orphan")
    tags: association_proxy = association_proxy("todo_tags", "tag")
    isDone: Mapped[bool]
    isArchived: Mapped[bool]
    createdAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completedAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    dueDate: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        result['tags'] = [tag.as_dict() for tag in self.tags]
        return result
    