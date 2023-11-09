from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas.lead import LeadBase, LeadUpdate
from app.models.lead import Lead
from datetime import datetime


class CRUDLead(CRUDBase):
    def get_by_biosignal(self, db: Session, *, biosignal_id: int, skip: int = 0, limit: int = 100) -> List[LeadBase]:
        return (
            db.query(self.model).filter(self.model.biosignal_id == biosignal_id).offset(skip).limit(limit).all()
        )

    def get_by_id(self, db: Session, *, id: int) -> LeadBase:
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, *, db_obj: LeadBase, obj_in: LeadUpdate) -> LeadBase:
        db_obj.name = obj_in.name
        db_obj.samples_number = obj_in.samples_number or db_obj.samples_number
        db_obj.signal = obj_in.signal or db_obj.signal
        db_obj.updated_at = datetime.now()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> LeadBase:
        db_obj = db.query(self.model).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj

    def create(self, db: Session, *, obj_in: LeadBase) -> LeadBase:
        samples_number = obj_in.samples_number or None
        db_obj = self.model(
            name=obj_in.name,
            biosignal_id=obj_in.biosignal_id,
            samples_number=samples_number,
            signal=obj_in.signal,
            created_at=datetime.now(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


lead = CRUDLead(Lead)
