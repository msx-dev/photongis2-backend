import uuid

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import ProjectInverter


class ElectricalString(Base):
    __tablename__ = "electrical_strings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_inverter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_inverters.id", ondelete="CASCADE"),
        nullable=False,
    )

    # [[[lat, lng], [lat, lng], ...], ...]
    design_lines: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    # ["polygon-id-1", "polygon-id-2", ...]
    connected_polygons: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    project_inverter: Mapped["ProjectInverter"] = relationship(
        "ProjectInverter",
        back_populates="strings",
    )