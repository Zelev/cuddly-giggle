from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .insight import Insight  # noqa: F401
    from .lead import Lead  # noqa: F401
    from .user import User  # noqa: F401


class Biosignal(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    leads = relationship(
        "Lead", back_populates="biosignal", cascade="all, delete-orphan"
    )
    insights = relationship(
        "Insight", back_populates="biosignal", cascade="all, delete-orphan"
    )
    created_at = Column(String, index=True, default=datetime.now(), nullable=False)
    updated_at = Column(String, index=True)
    user = relationship("User", back_populates="biosignals")
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
