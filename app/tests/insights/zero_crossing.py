from app.insights import zero_crossing
from app import crud
from app.schemas.lead import LeadCreate
from app.tests.utils.utils import random_lower_string
from app.tests.utils.biosignal import create_random_biosignal, create_random_biosignal_with_leads


def test_get_zero_crossing(db) -> None:
    biosignal = create_random_biosignal_with_leads(db)
    lead = biosignal.leads[0]
    insight = zero_crossing.get_zero_crossing(db, lead)
    assert insight.name == "Zero Crossing"
    assert insight.value_1 == 0
    assert insight.biosignal_id == biosignal.id

def test_get_zero_crossing_0_in_signal(db) -> None:
    biosignal = create_random_biosignal(db)
    # create a lead with a signal that has a zero crossing
    signal = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    lead_in = LeadCreate(name=random_lower_string(), signal=signal, biosignal_id=biosignal.id)
    lead = crud.lead.create(db=db, obj_in=lead_in)
    insight = zero_crossing.get_zero_crossing(db, lead)
    assert insight.name == "Zero Crossing"
    assert insight.value_1 == 1.0
    assert insight.biosignal_id == biosignal.id

def test_get_zero_crossing_no_0_in_signal(db) -> None:
    biosignal = create_random_biosignal(db)
    # create a lead with a signal that has no zero crossings
    signal = [-1, 2, 3, 4, 5, 6, 7, 8, 9]
    lead_in = LeadCreate(name=random_lower_string(), signal=signal, biosignal_id=biosignal.id)
    lead = crud.lead.create(db=db, obj_in=lead_in)
    insight = zero_crossing.get_zero_crossing(db, lead)
    assert insight.name == "Zero Crossing"
    assert insight.value_1 == 1.0
    assert insight.biosignal_id == biosignal.id

def test_get_zero_crossing_multiple_crossings(db) -> None:
    biosignal = create_random_biosignal(db)
    # create a lead with a signal that has multiple zero crossings
    # if the signal goes to 0 but keeps the sign afterwards, it is not a zero crossing
    signal = [-1, 0, 1, -3, 1, 0, 1, 2, 1, 5] 
    lead_in = LeadCreate(name=random_lower_string(), signal=signal, biosignal_id=biosignal.id)
    lead = crud.lead.create(db=db, obj_in=lead_in)
    insight = zero_crossing.get_zero_crossing(db, lead)
    assert insight.name == "Zero Crossing"
    assert insight.value_1 == 3.0
    assert insight.biosignal_id == biosignal.id

def test_get_zero_crossing_no_crossing_negative(db) -> None:
    biosignal = create_random_biosignal(db)
    # create a lead with a signal that has multiple zero crossings
    # if the signal goes to 0 but keeps the sign afterwards, it is not a zero crossing
    signal = [-1, 0, -1, -3, 1, 3, 1, 2, 1, 5] 
    lead_in = LeadCreate(name=random_lower_string(), signal=signal, biosignal_id=biosignal.id)
    lead = crud.lead.create(db=db, obj_in=lead_in)
    insight = zero_crossing.get_zero_crossing(db, lead)
    assert insight.name == "Zero Crossing"
    assert insight.value_1 == 1.0
    assert insight.biosignal_id == biosignal.id