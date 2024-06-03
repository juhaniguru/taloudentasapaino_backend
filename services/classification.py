from typing import Annotated

from fastapi import Depends

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



def get_classification_service(db: Db):
    return ClassificationService(db)


Classification = Annotated[ClassificationService, Depends(get_classification_service)]
