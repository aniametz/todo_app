from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import db

class TodoTagAssociation(db.Model):
    __tablename__ = "todo_tag_association"
    todo_id: Mapped[str] = mapped_column(ForeignKey('todo.id'), primary_key=True)
    tag_id: Mapped[str] = mapped_column(ForeignKey('tag.id'), primary_key=True)
    todo: Mapped["Todo"] = relationship(back_populates="todo_tags")
    tag: Mapped["Tag"] = relationship(back_populates="todo_tags")

    def __init__(self, tag=None, todo=None):
        self.tag = tag
        self.todo = todo
