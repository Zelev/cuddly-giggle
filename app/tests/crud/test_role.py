from sqlalchemy.orm import Session

from app import crud
from app.schemas.role import RoleCreate, RoleUpdate


def test_create_role(db: Session) -> None:
    # clean roles
    roles = crud.role.get_multi(db)
    for role in roles:
        if role.name not in ["admin", "client"]:
            crud.role.remove(db, id=role.id)

    name = "Test Role"
    description = "Test Role Description"
    role_in = RoleCreate(name=name, description=description)
    role = crud.role.create(db=db, obj_in=role_in)
    assert role.name == name
    assert role.description == description


def test_get_role(db: Session) -> None:
    # clean roles
    roles = crud.role.get_multi(db)
    for role in roles:
        if role.name not in ["admin", "client"]:
            crud.role.remove(db, id=role.id)

    name = "Test Role"
    description = "Test Role Description"
    role_in = RoleCreate(name=name, description=description)
    role = crud.role.create(db=db, obj_in=role_in)
    stored_role = crud.role.get(db=db, id=role.id)
    assert stored_role
    assert role.id == stored_role.id
    assert role.name == stored_role.name
    assert role.description == stored_role.description


def test_update_role(db: Session) -> None:
    # clean roles
    roles = crud.role.get_multi(db)
    for role in roles:
        if role.name not in ["admin", "client"]:
            crud.role.remove(db, id=role.id)

    name = "Test Role"
    description = "Test Role Description"
    role_in = RoleCreate(name=name, description=description)
    role = crud.role.create(db=db, obj_in=role_in)
    description2 = "Test Role Description 2"
    role_update = RoleUpdate(description=description2)
    role2 = crud.role.update(db=db, db_obj=role, obj_in=role_update)
    assert role.id == role2.id
    assert role.name == role2.name
    assert role2.description == description2


def test_delete_role(db: Session) -> None:
    # clean roles
    roles = crud.role.get_multi(db)
    for role in roles:
        if role.name not in ["admin", "client"]:
            crud.role.remove(db, id=role.id)

    name = "Test Role"
    description = "Test Role Description"
    role_in = RoleCreate(name=name, description=description)
    role = crud.role.create(db=db, obj_in=role_in)
    role2 = crud.role.remove(db=db, id=role.id)
    role3 = crud.role.get(db=db, id=role.id)
    assert role3 is None
    assert role2.id == role.id
    assert role2.name == name
    assert role2.description == description
