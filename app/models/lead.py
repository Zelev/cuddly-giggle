from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .biosignal import Biosignal  # noqa: F401


class Lead(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    samples_number = Column(Integer, index=True)
    signal = Column(ARRAY(Integer), index=True)
    created_at = Column(DateTime, index=True, default=datetime.now(), nullable=False)
    biosignal = relationship("Biosignal", back_populates="leads")
    biosignal_id = Column(Integer, ForeignKey("biosignal.id"))
    insights = relationship("Insight", back_populates="lead")
