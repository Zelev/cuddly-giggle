from sqlalchemy.orm import Session

from app import crud
from app.schemas.insight import InsightCreate, InsightUpdate
from app.tests.utils.biosignal import create_random_biosignal
from app.tests.utils.utils import random_lower_string


def test_create_insight(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    insight_in = InsightCreate(name=name, biosignal_id=biosignal.id)

    insight = crud.insight.create(db=db, obj_in=insight_in)
    assert insight.name == name
    assert insight.biosignal_id == biosignal.id


def test_get_insight(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    insight_in = InsightCreate(name=name, biosignal_id=biosignal.id)
    insight = crud.insight.create(db=db, obj_in=insight_in)
    stored_insight = crud.insight.get(db=db, id=insight.id)
    assert stored_insight
    assert insight.id == stored_insight.id
    assert insight.name == stored_insight.name
    assert insight.biosignal_id == stored_insight.biosignal_id


def test_get_insight_by_biosignal(db: Session) -> None:
    biosignal = create_random_biosignal(db)
    insight_in = InsightCreate(name=random_lower_string(), biosignal_id=biosignal.id)
    insight_1 = crud.insight.create(db=db, obj_in=insight_in)
    insight_in = InsightCreate(name=random_lower_string(), biosignal_id=biosignal.id)
    insight_2 = crud.insight.create(db=db, obj_in=insight_in)
    insights = crud.insight.get_by_biosignal(db=db, biosignal_id=biosignal.id)
    assert insights
    assert len(insights) == 2
    assert insight_1 in insights
    assert insight_2 in insights


def test_update_insight(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    insight_in = InsightCreate(name=name, biosignal_id=biosignal.id)
    insight = crud.insight.create(db=db, obj_in=insight_in)
    name2 = random_lower_string()
    insight_update = InsightUpdate(name=name2, id=insight.id)
    insight2 = crud.insight.update(db=db, db_obj=insight, obj_in=insight_update)
    assert insight.id == insight2.id
    assert name2 == insight2.name
    assert insight.biosignal_id == insight2.biosignal_id


def test_delete_insight(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    insight_in = InsightCreate(name=name, biosignal_id=biosignal.id)
    insight = crud.insight.create(db=db, obj_in=insight_in)
    insight2 = crud.insight.remove(db=db, id=insight.id)
    insight3 = crud.insight.get(db=db, id=insight.id)
    assert insight3 is None
    assert insight2.id == insight.id
    assert insight2.name == name