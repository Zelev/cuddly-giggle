from typing import Optional

from pydantic import ConfigDict, BaseModel


class InsightBase(BaseModel):
    name: str
    description: Optional[str] = None
    value_1: Optional[float] = None
    value_2: Optional[bool] = None
    value_3: Optional[str] = None


class InsightCreate(InsightBase):
    biosignal_id: int
    name: str
    description: Optional[str] = None
    value_1: Optional[float] = None
    value_2: Optional[bool] = None
    value_3: Optional[str] = None


class InsightUpdate(InsightBase):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    value_1: Optional[float] = None
    value_2: Optional[bool] = None
    value_3: Optional[str] = None


class InsightInDBBase(InsightBase):
    id: int
    name: str
    description: Optional[str] = None
    value_1: Optional[float] = None
    value_2: Optional[bool] = None
    value_3: Optional[str] = None
    biosignal_id: int
    model_config = ConfigDict(from_attributes=True)


class Insight(InsightInDBBase):
    pass
