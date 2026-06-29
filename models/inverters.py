import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User


class Inverter(Base):
    __tablename__ = "inverters"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now()
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Power limits
    max_ac_power: Mapped[int] = mapped_column(Integer, nullable=False)   # W
    max_dc_power: Mapped[int] = mapped_column(Integer, nullable=False)   # W

    # Voltage limits
    max_dc_voltage: Mapped[int] = mapped_column(Integer, nullable=False)  # V
    mppt_min_voltage: Mapped[int] = mapped_column(Integer, nullable=False) # V
    mppt_max_voltage: Mapped[int] = mapped_column(Integer, nullable=False) # V
    start_voltage: Mapped[int] = mapped_column(Integer, nullable=True)     # V

    # Current limits (critical for string parallelization)
    max_current_per_mppt: Mapped[float] = mapped_column(Float, nullable=True)  # A

    # MPPT structure
    mppt_count: Mapped[int] = mapped_column(Integer, nullable=True)

    # Optional constraint (kept flexible)
    max_strings_per_mppt: Mapped[int] = mapped_column(Integer, nullable=True)

    # Efficiency
    efficiency: Mapped[float] = mapped_column(Float, nullable=True)  # e.g. 0.97

    owner: Mapped["User"] = relationship("User")