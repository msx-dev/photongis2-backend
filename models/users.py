import uuid
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Project


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="owner", cascade="all, delete-orphan"
    )
