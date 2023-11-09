from typing import Dict

from sqlalchemy.orm import Session

from app import crud, models
from app.tests.utils.utils import random_lower_string, random_email
from app.schemas.user import UserCreate
from app.schemas.biosignal import BiosignalCreate, Biosignal
from app.schemas.lead import LeadCreate
from app.schemas.insight import InsightCreate


def create_random_biosignal(db: Session, *, user_id: int = None) -> models.Biosignal:
    if user_id is None:
        # get client role by name
        role = crud.role.get_by_name(db, name="client")
        # create client user
        user = crud.user.create(
            db=db,
            obj_in=UserCreate(
                email=random_email(),
                password="superawesometestpassword",
                role_id=role.id,
            ),
        )
        user_id = user.id
    biosignal_in = BiosignalCreate(name=random_lower_string(), user_id=user_id)
    return crud.biosignal.create(db=db, obj_in=biosignal_in)


def create_random_biosignal_with_leads(
    db: Session, *, user_id: int = None
) -> Biosignal:
    biosignal = create_random_biosignal(db=db, user_id=user_id)
    lead_in = LeadCreate(name=random_lower_string(), biosignal_id=biosignal.id)
    crud.lead.create(db=db, obj_in=lead_in)
    return biosignal


def create_random_biosignal_with_leads_and_insigths(
    db: Session, *, user_id: int = None
) -> Biosignal:
    biosignal = create_random_biosignal(db=db, user_id=user_id)
    lead_in = LeadCreate(
        name=random_lower_string(),
        biosignal_id=biosignal.id,
        signal=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )
    crud.lead.create(db=db, obj_in=lead_in)
    insight_in = InsightCreate(name=random_lower_string(), biosignal_id=biosignal.id)
    insight_in = crud.insight.create(db=db, obj_in=insight_in)
    crud.insight.create(db=db, obj_in=insight_in)
    db.commit()
    db.refresh(biosignal)
    return biosignal
