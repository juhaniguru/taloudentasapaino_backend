from fastapi import APIRouter, Path

from dtos.expenses import CreateExpenseReq, ExpenseRes
from services.expense import Expense

router = APIRouter(
    prefix='/api/v1/expenses',
    tags=['expenses']
)


@router.get('/{expense_id}')
async def get_expense(service: Expense, expense_id: int = Path(gt=0)) -> ExpenseRes:
    expense = service.get_expense(expense_id)
    return expense


@router.get('/{year}/{month}')
async def get_expenses_by_year_and_month(service: Expense, year: int, month: int = Path(gt=0, lt=13)):
    expenses = service.get_expenses_by_year_month_type(year, month)

    return expenses


@router.put('/{expense_id}')
async def edit_expense(service: Expense, req: CreateExpenseReq, expense_id: int) -> ExpenseRes:
    expense = service.edit_expense(expense_id, req)
    return expense


@router.delete('/{expense_id}')
async def delete_expense(service: Expense, expense_id: int):
    service.delete_expense(expense_id)
    return None
