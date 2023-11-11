import json
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.insights import get_total_zero_crossing, get_zero_crossing

router = APIRouter()


@router.post("/", response_model=Any)
def create_biosignal(
    *,
    db: Session = Depends(deps.get_db),
    biosignal_in: schemas.BiosignalCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new biosignal.
    """
    # Verify that the user is a client role
    user = crud.user.get(db, id=current_user.id)
    if not user.role.name == "client":  # this would be better with enums
        raise HTTPException(status_code=403, detail="Not enough permissions")
    biosignal_obj = crud.biosignal.create(db=db, obj_in=biosignal_in)
    # create the leads from the info in the biosignal
    if biosignal_in.leads:
        for lead in biosignal_in.leads:
            lead.biosignal_id = biosignal_obj.id
            lead_obj = crud.lead.create(db=db, obj_in=lead)
            # calculate the insights for the biosignal by each lead
            get_zero_crossing(db=db, lead=lead_obj)
        get_total_zero_crossing(db=db, biosignal=biosignal_obj)
    # Assemble the response since the serializer is mocking me
    insights = assemble_insights(biosignal_obj.insights)
    leads = assemble_leads(biosignal_obj.leads)
    response = {
        "id": biosignal_obj.id,
        "name": biosignal_obj.name,
        "user_id": biosignal_obj.user_id,
        "leads": leads,
        "insights": insights,
    }
    return json.dumps(response)


@router.get("/", response_model=List[schemas.Biosignal])
def read_biosignals(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve biosignals.
    """
    # Verify that the user is a client role
    user = crud.user.get(db, id=current_user.id)
    if not user.role.name == "client":  # this would be better with enums
        raise HTTPException(status_code=403, detail="Not enough permissions")
    # Get the biosignals only for the current user
    biosignals = crud.biosignal.get_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return biosignals


@router.get("/{id}", response_model=Any)
def read_biosignal(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get biosignal by ID.
    """
    # Verify that the user is a client role
    user = crud.user.get(db, id=current_user.id)
    if not user.role.name == "client":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    biosignal = crud.biosignal.get(db=db, id=id)
    if biosignal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    if not biosignal:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    # Assemble the response since the serializer is mocking me
    insights = assemble_insights(biosignal.insights)
    leads = assemble_leads(biosignal.leads)
    response = {
        "id": biosignal.id,
        "name": biosignal.name,
        "user_id": biosignal.user_id,
        "leads": leads,
        "insights": insights,
    }
    return response


@router.put("/{id}", response_model=Any)
def update_biosignal(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    biosignal_in: schemas.BiosignalUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a biosignal.
    """
    # Verify that the user is a client role
    user = crud.user.get(db, id=current_user.id)
    if not user.role.name == "client":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    biosignal = crud.biosignal.get(db=db, id=id)
    if biosignal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    if not biosignal:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    biosignal = crud.biosignal.update(db=db, db_obj=biosignal, obj_in=biosignal_in)
    # Assemble the response since the serializer is mocking me
    insights = assemble_insights(biosignal.insights)
    leads = assemble_leads(biosignal.leads)
    response = {
        "id": biosignal.id,
        "name": biosignal.name,
        "user_id": biosignal.user_id,
        "leads": leads,
        "insights": insights,
    }
    return json.dumps(response)


@router.delete("/{id}", response_model=schemas.Biosignal)
def delete_biosignal(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a biosignal.
    """
    # Verify that the user is a client role
    user = crud.user.get(db, id=current_user.id)
    if not user.role.name == "client":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    biosignal = crud.biosignal.get(db=db, id=id)
    if biosignal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    if not biosignal:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    biosignal = crud.biosignal.remove(db=db, id=id)
    return biosignal


def assemble_leads(leads: List[models.Lead]) -> List[dict]:
    return [
        {
            "id": lead_obj.id,
            "name": lead_obj.name,
            "signal": lead_obj.signal,
            "insights": assemble_insights(lead_obj.insights),
        }
        for lead_obj in leads
    ]


def assemble_insights(insights: List[models.Insight]) -> List[dict]:
    return [
        {
            "id": insight_obj.id,
            "name": insight_obj.name,
            "description": insight_obj.description,
            "value_1": insight_obj.value_1,
            "value_2": insight_obj.value_2,
            "value_3": insight_obj.value_3,
        }
        for insight_obj in insights
    ]
