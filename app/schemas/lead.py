from typing import Optional

from pydantic import ConfigDict, BaseModel


class LeadBase(BaseModel):
    name: str
    samples_number: Optional[int] = None
    signal: list[int] = []


class LeadCreate(LeadBase):
    biosignal_id: Optional[int] = None


class LeadUpdate(LeadBase):
    signal: Optional[list[int]] = None


class LeadInDBBase(LeadBase):
    id: int
    name: str
    biosignal_id: int
    samples_number: Optional[int] = None
    signal: list[int] = []
    model_config = ConfigDict(from_attributes=True)


class Lead(LeadInDBBase):
    pass
