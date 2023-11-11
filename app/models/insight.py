from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .biosignal import Biosignal  # noqa: F401


class Insight(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, index=True, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, index=True)
    biosignal = relationship("Biosignal", back_populates="insights")
    biosignal_id = Column(Integer, ForeignKey("biosignal.id"))
    value_1 = Column(Float, index=True)
    value_2 = Column(Boolean, index=True)
    value_3 = Column(String, index=True)
    lead_id = Column(Integer, ForeignKey("lead.id"))
    lead = relationship("Lead", back_populates="insights")
