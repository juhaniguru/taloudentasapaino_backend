from typing import List
from fastapi import APIRouter
from dtos.classifications import CreateClassificationReq, ClassificationRes
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


@router.put('/{classification_id}')
async def edit_classification(classification_id: int, req: CreateClassificationReq,
                              service: Classification) -> ClassificationRes:
    c = service.edit_classification(classification_id, req)

    return c


@router.delete('/{classification_id}')
async def delete_classification(classification_id: int,
                                service: Classification):
    service.delete_classification(classification_id)
    return ""


@router.get('/{classification_id}')
async def get_classification(classification_id: int,
                                service: Classification) -> ClassificationRes:
    c = service.get_classification(classification_id)
    return c
