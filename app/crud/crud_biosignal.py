from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.biosignal import Biosignal
from app.schemas.biosignal import BiosignalCreate, BiosignalUpdate
from datetime import datetime


class CRUDBiosignal(CRUDBase[Biosignal, BiosignalCreate, BiosignalUpdate]):
    def create(self, db: Session, *, obj_in: BiosignalCreate) -> Biosignal:
        db_obj = Biosignal(
            name=obj_in.name,
            user_id=obj_in.user_id,
            created_at=datetime.now(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Biosignal,
        obj_in: Union[BiosignalUpdate, Dict[str, Any]]
    ) -> Biosignal:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        # update leads if provided
        update_data["updated_at"] = datetime.now()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self, db: Session, *, id: int) -> Biosignal:
        db_obj = db.query(Biosignal).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj

    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> Optional[Biosignal]:
        return db.query(Biosignal).filter(Biosignal.user_id == user_id).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Biosignal]:
        return db.query(Biosignal).filter(Biosignal.id == id).first()


biosignal = CRUDBiosignal(Biosignal)
