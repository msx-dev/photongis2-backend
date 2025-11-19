from database import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import uuid
from datetime import datetime
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from models import User, Rooftop


class Panel(Base):
    __tablename__ = "panels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    name: Mapped[str] = mapped_column(String(50), nullable=True)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    power: Mapped[int] = mapped_column(Integer, nullable=False)

    rooftops: Mapped[list["Rooftop"]] = relationship("Rooftop", back_populates="panel")
    owner: Mapped["User"] = relationship("User", back_populates="panels")
