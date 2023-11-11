from sqlalchemy.orm import Session

from app import crud, models
from app.insights import get_zero_crossing
from app.schemas.lead import LeadCreate
from app.tests.utils.biosignal import create_random_biosignal
from app.tests.utils.utils import random_lower_string


def create_random_lead(db: Session, *, biosignal_id: int = None) -> models.Lead:
    if biosignal_id is None:
        biosignal = create_random_biosignal(db)
        biosignal_id = biosignal.id
    lead_in = LeadCreate(name=random_lower_string(), biosignal_id=biosignal_id)
    return crud.lead.create(db=db, obj_in=lead_in)


def create_random_lead_with_insight(
    db: Session, *, biosignal_id: int = None
) -> models.Lead:
    lead = create_random_lead(
        db, biosignal_id=biosignal_id, signal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    get_zero_crossing(db, lead)
    return lead
