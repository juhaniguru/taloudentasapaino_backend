from fastapi import APIRouter, Path

from dtos.expenses import CreateExpenseReq, ExpenseRes
from services.expense import Expense

router = APIRouter(
    prefix='/api/v1/expenses',
    tags=['expenses']
)


@router.get('/{expense_id}')
async def get_expense(service: Expense, expense_id: int = Path(gt=0)) -> ExpenseRes:

    """ Yksittäisen kulun haku"""

    expense = service.get_expense(expense_id)
    return expense


@router.get('/grouped/{year}/{month}')
async def get_grouped_expenses_by_year_and_month(service: Expense, year: int, month: int = Path(gt=0, lt=13)):

    """ Kulujen yhteissumman hakeminen vuoden ja kuukauden perusteella"""

    expenses = service.get_grouped_expenses_by_year_month_type(year, month)

    return expenses


@router.get('/{year}/{month}')
async def get_expenses_by_year_month(service: Expense, year: int, month: int = Path(gt=0, lt=13)):

    """ Kaikkien kulujen listaaminen kuukauden ja vuoden perusteella"""

    expenses = service.get_expenses_by_year_month(year, month)



    return expenses


@router.put('/{expense_id}')
async def edit_expense(service: Expense, req: CreateExpenseReq, expense_id: int) -> ExpenseRes:
    """ Kulun muokkaaminen"""

    expense = service.edit_expense(expense_id, req)
    return expense


@router.delete('/{expense_id}')
async def delete_expense(service: Expense, expense_id: int):
    """ Kulun poisto"""
    service.delete_expense(expense_id)
    return None
