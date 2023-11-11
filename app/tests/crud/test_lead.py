from sqlalchemy.orm import Session

from app import crud
from app.insights import get_zero_crossing
from app.schemas.lead import LeadCreate, LeadUpdate
from app.tests.utils.biosignal import create_random_biosignal
from app.tests.utils.utils import random_lower_string


def test_create_lead(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    lead_in = LeadCreate(name=name, biosignal_id=biosignal.id)

    lead = crud.lead.create(db=db, obj_in=lead_in)
    assert lead.name == name
    assert lead.biosignal_id == biosignal.id


def test_get_lead(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    lead_in = LeadCreate(name=name, biosignal_id=biosignal.id)
    lead = crud.lead.create(db=db, obj_in=lead_in)
    stored_lead = crud.lead.get(db=db, id=lead.id)
    assert stored_lead
    assert lead.id == stored_lead.id
    assert lead.name == stored_lead.name
    assert lead.biosignal_id == stored_lead.biosignal_id


def test_get_lead_by_biosignal_id(db: Session) -> None:
    biosignal = create_random_biosignal(db)
    lead_in = LeadCreate(name=random_lower_string(), biosignal_id=biosignal.id)
    lead_1 = crud.lead.create(db=db, obj_in=lead_in)
    lead_in = LeadCreate(name=random_lower_string(), biosignal_id=biosignal.id)
    lead_2 = crud.lead.create(db=db, obj_in=lead_in)
    leads = crud.lead.get_by_biosignal(db=db, biosignal_id=biosignal.id)
    assert leads
    assert len(leads) == 2
    assert lead_1 in leads
    assert lead_2 in leads


def test_update_lead(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    lead_in = LeadCreate(name=name, biosignal_id=biosignal.id)
    lead = crud.lead.create(db=db, obj_in=lead_in)
    name2 = random_lower_string()
    lead_update = LeadUpdate(name=name2)
    lead2 = crud.lead.update(db=db, db_obj=lead, obj_in=lead_update)
    assert lead.id == lead2.id
    assert name2 == lead2.name
    assert lead.biosignal_id == lead2.biosignal_id


def test_delete_lead(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    lead_in = LeadCreate(name=name, biosignal_id=biosignal.id)
    lead = crud.lead.create(db=db, obj_in=lead_in)
    lead2 = crud.lead.remove(db=db, id=lead.id)
    lead3 = crud.lead.get(db=db, id=lead.id)
    assert lead3 is None
    assert lead2.id == lead.id
    assert lead2.name == name
    assert lead2.biosignal_id == biosignal.id


def test_get_lead_with_insight(db: Session) -> None:
    name = random_lower_string()
    biosignal = create_random_biosignal(db)
    lead_in = LeadCreate(
        name=name, biosignal_id=biosignal.id, signal=[-1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
    lead_obj = crud.lead.create(db=db, obj_in=lead_in)
    get_zero_crossing(db, lead_obj)
    lead = crud.lead.get(db=db, id=lead_obj.id)
    assert lead
    assert lead.insights
    assert len(lead.insights) == 1
    assert lead.insights[0].name == "Zero Crossing"
    assert lead.insights[0].value_1 == 1.0
