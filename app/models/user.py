from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .role import Role  # noqa: F401
    from .biosignal import Biosignal  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
    biosignals = relationship(
        "Biosignal", back_populates="user", cascade="all, delete-orphan"
    )
    role = relationship("Role", back_populates="users")
    role_id = Column(Integer, ForeignKey("role.id"))
    created_at = Column(DateTime, default=datetime.now())
