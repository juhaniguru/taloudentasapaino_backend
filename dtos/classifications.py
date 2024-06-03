from typing import List

from pydantic import BaseModel


class CreateClassificationReq(BaseModel):
    name: str
    expense_type: str


class ClassificationRes(CreateClassificationReq):
    id: int


class ClassificationsRes(BaseModel):
    classifications: List[ClassificationRes]
