from typing import Annotated

from fastapi import Depends, HTTPException

import models
from dtos.classifications import CreateClassificationReq
from models import Db
from services.base import BaseService


class ClassificationService(BaseService):
    def __init__(self, db: Db):
        super(ClassificationService, self).__init__(db)

    def get_all_classifications(self):
        return self.db.query(models.ExpenseClassifications).all()

    def create_classification(self, req: CreateClassificationReq) -> models.ExpenseClassifications:
        c = models.ExpenseClassifications(**req.model_dump())
        self.db.add(c)
        self.db.commit()

        return c

    def get_classification(self, _id):
        return self._get_by_id(_id)

    def _get_by_id(self, _id):
        c = self.db.query(models.ExpenseClassifications).filter_by(id=_id).first()
        if c is None:
            raise HTTPException(status_code=404, detail="Expense classification not found")
        return c

    def edit_classification(self, classification_id: int,
                            req: CreateClassificationReq) -> models.ExpenseClassifications:
        c = self._get_by_id(classification_id)
        c.name = req.name
        c.expense_type = req.expense_type
        self.db.commit()

        return c

    def delete_classification(self, classification_id: int) -> bool:
        c = self._get_by_id(classification_id)
        self.db.delete(c)
        self.db.commit()

        return True


def get_classification_service(db: Db):
    return ClassificationService(db)


Classification = Annotated[ClassificationService, Depends(get_classification_service)]
