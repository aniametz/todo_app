from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import db
import uuid

class Priority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Todo(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    description: Mapped[str] = mapped_column(unique=True)
    priority: Mapped[str] = mapped_column(nullable=True)
    isDone: Mapped[bool]
    isArchived: Mapped[bool]
    createdAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completedAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}