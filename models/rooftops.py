from database import Base
from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Project


class Rooftop(Base):
    __tablename__ = "rooftops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE")
    )

    polygon: Mapped[list] = mapped_column(JSONB, nullable=False)
    angle: Mapped[float] = mapped_column(Float, nullable=False)
    slope: Mapped[float] = mapped_column(Float, nullable=False)

    project: Mapped["Project"] = relationship("Project", back_populates="rooftops")
