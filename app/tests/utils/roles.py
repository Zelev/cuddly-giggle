from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from app.tests.utils.utils import random_lower_string


def create_random_role(db: Session) -> Role:
    name = random_lower_string()
    description = random_lower_string()
    role_in = RoleCreate(name=name, description=description)
    role = crud.role.create(db=db, obj_in=role_in)
    return role


def create_admin_role(db: Session) -> Role:
    name = "Admin"
    description = "Admin Role"
    role_in = RoleCreate(name=name, description=description)
    role = crud.role.create(db=db, obj_in=role_in)
    return role
