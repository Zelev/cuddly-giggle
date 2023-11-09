from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    for role_name in ["admin", "client"]:
        role = crud.role.get_by_name(db, name=role_name)

        if not role:
            role_in = schemas.RoleCreate(
                name=role_name, description=f"{role_name} role"
            )
            role = crud.role.create(db, obj_in=role_in)

    role = crud.role.get_by_name(db, name="admin")
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)

    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            role_id=role.id,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
