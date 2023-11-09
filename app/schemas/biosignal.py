from typing import Optional

from pydantic import ConfigDict, BaseModel
from app.schemas.lead import Lead, LeadCreate, LeadUpdate
from app.schemas.insight import Insight


# Shared properties
class BiosignalBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class BiosignalCreate(BiosignalBase):
    name: str
    user_id: int
    leads: Optional[list[LeadCreate]] = None


# Properties to receive via API on update
class BiosignalUpdate(BiosignalBase):
    leads: Optional[list[LeadUpdate]] = None


class BiosignalInDB(BiosignalBase):
    id: int
    name: str
    user_id: int
    leads: Optional[list[Lead]] = None
    insights: Optional[list[Insight]] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Biosignal(BiosignalInDB):
    pass