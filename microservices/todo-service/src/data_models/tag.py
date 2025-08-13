from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from database import db
from data_models.todo_tag_association import TodoTagAssociation
import uuid

class Tag(db.Model):
    __tablename__ = "tag"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(unique=True)
    color: Mapped[str] = mapped_column(default="#000000")
    todo_tags: Mapped[List[TodoTagAssociation]] = relationship("TodoTagAssociation", back_populates="tag", cascade="all, delete-orphan")
    todos: association_proxy = association_proxy("todo_tags", "todo")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}