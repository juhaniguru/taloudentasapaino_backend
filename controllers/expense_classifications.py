from typing import List
from fastapi import APIRouter, Depends

from dependencies import OptionalAccount, require_logged_in_user
from dtos.classifications import CreateClassificationReq, ClassificationRes, ClassificationsRes
from dtos.expenses import ExpenseRes, CreateExpenseReq
from services.classification import Classification
from services.expense import Expense

router = APIRouter(
    prefix='/api/v1/classifications',
    tags=['classifications']
)


@router.get('/')
async def get_classifications(service: Classification) -> dict[str, List[ClassificationRes]]:
    classifications = service.get_all_classifications()

    return {'classifications': classifications}


@router.post('/', dependencies=[Depends(require_logged_in_user)])
async def create_classification(req: CreateClassificationReq, service: Classification) -> ClassificationRes:
    c = service.create_classification(req)

    return c


@router.put('/{classification_id}', dependencies=[Depends(require_logged_in_user)])
async def edit_classification(classification_id: int, req: CreateClassificationReq,
                              service: Classification) -> ClassificationRes:
    c = service.edit_classification(classification_id, req)

    return c


@router.delete('/{classification_id}', dependencies=[Depends(require_logged_in_user)])
async def delete_classification(classification_id: int,
                                service: Classification):
    service.delete_classification(classification_id)
    return ""


@router.get('/{classification_id}', dependencies=[Depends(require_logged_in_user)])
async def get_classification(classification_id: int,
                             service: Classification) -> ClassificationRes:
    c = service.get_classification(classification_id)
    return c


@router.get('/{classification_id}/expenses', dependencies=[Depends(require_logged_in_user)])
async def get_expenses_by_classification(classification_id: int,
                                         service: Expense) -> dict[str, List[ExpenseRes]]:
    expenses = service.get_all_expenses_by_classification(classification_id)
    return {'expenses': expenses}


@router.post('/{classification_id}/expenses')
async def create_expense(classification_id: int, account: OptionalAccount, req: CreateExpenseReq,
                      service: Expense) -> ExpenseRes:
    c = service.create_expense(classification_id, account, req)
    return c
