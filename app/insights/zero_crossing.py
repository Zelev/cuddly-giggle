from app import crud
from app.schemas.insight import InsightCreate
from app.schemas.lead import Lead


import numpy


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
    insight_in = InsightCreate(name="Zero Crossing", value_1=zero_crossings_count, biosignal_id=lead.biosignal_id)
    return crud.insight.create(db=db, obj_in=insight_in)