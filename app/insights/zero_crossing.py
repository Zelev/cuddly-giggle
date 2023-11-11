import numpy

from app import crud
from app.schemas.biosignal import Biosignal
from app.schemas.insight import InsightCreate
from app.schemas.lead import Lead


def get_zero_crossing(db, lead: Lead) -> InsightCreate:
    """
    Given an array of int or float, return the number of zero crossings
    If the sequence touches zero but does not cross, is nmot considered as a crossing.

    Steps:
    1. Load the signal from the lead
    2. Remove the 0s from the signal
    3. Convert the array to a boolean array where True is negative sign and False is positive
    4. Find the indexes where the signal crosses the zero line
    5. Count the number of crossings
    6. Create the insight and return it
    """
    # the elements '0' are considered as possitive, therefore we need to remove them
    # to keep the consistency of the cases where the signal goes to 0 but does not cross
    # load signal and remove 0s
    signal = numpy.array(lead.signal)
    signal = signal[signal != 0]
    # this returns the list of indexes just before the zero crossing
    zero_crossings = numpy.where(numpy.diff(numpy.signbit(signal)))[0]
    zero_crossings_count = len(zero_crossings) or 0
    insight_in = InsightCreate(
        name="Zero Crossing", value_1=zero_crossings_count, lead_id=lead.id
    )
    return crud.insight.create(db=db, obj_in=insight_in)


def get_total_zero_crossing(db, biosignal: Biosignal) -> InsightCreate:
    """
    In case that the Biosignal has more than one lead, this function will return the total
    number of zero crossings for all the leads in the Biosignal
    """
    crossings = []
    for lead in biosignal.leads:
        crossings = [
            insight for insight in lead.insights if insight.name == "Zero Crossing"
        ]
    insight_in = InsightCreate(
        name="Total Zero Crossing",
        value_1=sum([insight.value_1 for insight in crossings]),
        biosignal_id=biosignal.id,
    )
    return crud.insight.create(db=db, obj_in=insight_in)
