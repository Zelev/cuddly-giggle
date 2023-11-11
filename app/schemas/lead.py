from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.insight import Insight


class LeadBase(BaseModel):
    name: str
    samples_number: Optional[int] = None
    signal: list[int] = []


class LeadCreate(LeadBase):
    biosignal_id: Optional[int] = None


class LeadUpdate(LeadBase):
    signal: Optional[list[int]] = None
    insights: Optional[list[Insight]] = None


class LeadInDBBase(LeadBase):
    id: int
    name: str
    biosignal_id: int
    samples_number: Optional[int] = None
    signal: list[int] = []
    insights: Optional[list[Insight]]
    model_config = ConfigDict(from_attributes=True)


class Lead(LeadInDBBase):
    id: int
    name: str
    samples_number: Optional[int] = None
    signal: list[int] = []
    insights: Optional[list[Insight]] = None
