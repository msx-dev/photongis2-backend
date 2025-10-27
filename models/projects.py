from database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Rooftop, User


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )

    name: Mapped[str] = mapped_column(String(50), nullable=True)

    rooftops: Mapped[list["Rooftop"]] = relationship(
        "Rooftop", back_populates="project", cascade="all, delete-orphan"
    )

    owner: Mapped["User"] = relationship("User", back_populates="projects")
