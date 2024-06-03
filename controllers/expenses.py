from fastapi import APIRouter

from dtos.expenses import CreateExpenseReq, ExpenseRes
from services.expense import Expense

router = APIRouter(
    prefix='/api/v1/expenses',
    tags=['expenses']
)


@router.get('/{expense_id}')
async def get_expense(service: Expense, expense_id: int) -> ExpenseRes:
    expense = service.get_expense(expense_id)
    return expense


@router.put('/{expense_id}')
async def get_expense(service: Expense, req: CreateExpenseReq, expense_id: int) -> ExpenseRes:
    expense = service.edit_expense(expense_id, req)
    return expense


@router.delete('/{expense_id}')
async def delete_expense(service: Expense, expense_id: int):
    service.delete_expense(expense_id)
    return None
