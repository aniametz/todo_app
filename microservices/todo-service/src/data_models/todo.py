from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database import db
import uuid

class Todo(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    description: Mapped[str] = mapped_column(unique=True)
    isDone: Mapped[bool]
    isArchived: Mapped[bool]

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}