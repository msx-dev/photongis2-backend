import uuid

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Project, Inverter, ElectricalString


class ProjectInverter(Base):
    __tablename__ = "project_inverters"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    inverter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("inverters.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="project_inverters",
    )

    inverter: Mapped["Inverter"] = relationship("Inverter")

    strings: Mapped[list["ElectricalString"]] = relationship(
        "ElectricalString",
        back_populates="project_inverter",
        cascade="all, delete-orphan",
    )