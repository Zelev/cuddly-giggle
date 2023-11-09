from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.insights import get_zero_crossing

router = APIRouter()


@router.post("/", response_model=schemas.Biosignal)
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
    biosignal = crud.biosignal.create(db=db, obj_in=biosignal_in)
    # create the leads from the info in the biosignal
    if biosignal_in.leads:
        for lead in biosignal_in.leads:
            lead.biosignal_id = biosignal.id
            lead_obj = crud.lead.create(db=db, obj_in=lead)
            # calculate the insights for the biosignal by each lead
            get_zero_crossing(db=db, lead=lead_obj)
    return biosignal


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


@router.get("/{id}", response_model=schemas.Biosignal)
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
    biosignal = crud.biosignal.get_by_id(db=db, id=id)
    if biosignal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    if not biosignal:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    return biosignal


@router.put("/{id}", response_model=schemas.Biosignal)
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
    biosignal = crud.biosignal.get_by_id(db=db, id=id)
    if biosignal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    if not biosignal:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    biosignal = crud.biosignal.update(db=db, db_obj=biosignal, obj_in=biosignal_in)
    return biosignal


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
    biosignal = crud.biosignal.get_by_id(db=db, id=id)
    if biosignal.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    if not biosignal:
        raise HTTPException(status_code=404, detail="Biosignal not found")
    biosignal = crud.biosignal.remove(db=db, id=id)
    return biosignal
