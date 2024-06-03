from typing import Dict, List, Type

from fastapi import APIRouter

from dependencies import Account
from dtos.auth import LoginReq, LoginRes, RegisterRes, GetAccountRes
from dtos.classifications import ClassificationsRes, CreateClassificationReq, ClassificationRes
from models import ExpenseClassifications
from services.auth import Auth
from services.classification import Classification

router = APIRouter(
    prefix='/api/v1/classifications',
    tags=['classifications']
)


@router.get('/')
async def get_classifications(service: Classification) -> dict[str, List[ClassificationRes]]:
    classifications = service.get_all_classifications()

    return {'classifications': classifications}


@router.post('/')
async def create_classification(req: CreateClassificationReq, service: Classification) -> ClassificationRes:
    c = service.create_classification(req)

    return c
