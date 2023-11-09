from sqlalchemy.orm import Session

from app import crud
from app.schemas.biosignal import BiosignalCreate, BiosignalUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_biosignal(db: Session) -> None:
    name = random_lower_string()
    user = create_random_user(db)
    biosignal_in = BiosignalCreate(name=name, user_id=user.id)

    biosignal = crud.biosignal.create(db=db, obj_in=biosignal_in)
    assert biosignal.name == name
    assert biosignal.user_id == user.id


def test_get_biosignal(db: Session) -> None:
    name = random_lower_string()
    user = create_random_user(db)
    biosignal_in = BiosignalCreate(name=name, user_id=user.id)
    biosignal = crud.biosignal.create(db=db, obj_in=biosignal_in)
    stored_biosignal = crud.biosignal.get(db=db, id=biosignal.id)
    assert stored_biosignal
    assert biosignal.id == stored_biosignal.id
    assert biosignal.name == stored_biosignal.name
    assert biosignal.user_id == stored_biosignal.user_id


def test_update_biosignal(db: Session) -> None:
    name = random_lower_string()
    user = create_random_user(db)
    biosignal_in = BiosignalCreate(name=name, user_id=user.id)
    biosignal = crud.biosignal.create(db=db, obj_in=biosignal_in)
    name2 = random_lower_string()
    biosignal_update = BiosignalUpdate(name=name2)
    biosignal2 = crud.biosignal.update(db=db, db_obj=biosignal, obj_in=biosignal_update)
    assert biosignal.id == biosignal2.id
    assert name2 == biosignal2.name
    assert biosignal.user_id == biosignal2.user_id


def test_delete_biosignal(db: Session) -> None:
    name = random_lower_string()
    user = create_random_user(db)
    biosignal_in = BiosignalCreate(name=name, user_id=user.id)
    biosignal = crud.biosignal.create(db=db, obj_in=biosignal_in)
    biosignal2 = crud.biosignal.remove(db=db, id=biosignal.id)
    biosignal3 = crud.biosignal.get(db=db, id=biosignal.id)
    assert biosignal3 is None
    assert biosignal2.id == biosignal.id
    assert biosignal2.name == name
