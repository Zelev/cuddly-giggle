from typing import Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class RoleBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Properties to receive via API on creation
class RoleCreate(RoleBase):
    name: str


# Properties to receive via API on update
class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Role(RoleInDBBase):
    pass


# Additional properties stored in DB
class RoleInDB(RoleInDBBase):
    pass
