from database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from models import Rooftop, User


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )

    name: Mapped[str] = mapped_column(String(50), nullable=True)

    rooftops: Mapped[list["Rooftop"]] = relationship(
        "Rooftop", back_populates="project", cascade="all, delete-orphan"
    )

    owner: Mapped["User"] = relationship("User", back_populates="projects")
