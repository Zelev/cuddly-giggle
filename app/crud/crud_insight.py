from app.crud.base import CRUDBase

from app.models.insight import Insight
from app.schemas.insight import InsightCreate, InsightUpdate

from datetime import datetime

class CRUDInsight(CRUDBase[Insight, InsightCreate, InsightUpdate]):
    def create(
        self, db, *, obj_in: InsightCreate
    ) -> Insight:
        db_obj = Insight(
            name=obj_in.name,
            description=obj_in.description,
            value_1=obj_in.value_1,
            value_2=obj_in.value_2,
            value_3=obj_in.value_3,
            biosignal_id=obj_in.biosignal_id,
            created_at=datetime.now(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db,
        *,
        db_obj: Insight,
        obj_in: InsightUpdate
    ) -> Insight:
        db_obj.name = obj_in.name or db_obj.name
        db_obj.description = obj_in.description or db_obj.description
        db_obj.value_1 = obj_in.value_1 or db_obj.value_1
        db_obj.value_2 = obj_in.value_2 or db_obj.value_2
        db_obj.value_3 = obj_in.value_3 or db_obj.value_3
        db_obj.updated_at = datetime.now()
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db, *, id: int) -> Insight:
        db_obj = db.query(self.model).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj
    
    def get(self, db, *, id: int) -> Insight:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_by_biosignal(self, db, *, biosignal_id: int) -> Insight:
        return db.query(self.model).filter(self.model.biosignal_id == biosignal_id).all()
    

insight = CRUDInsight(Insight)