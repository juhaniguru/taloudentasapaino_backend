from datetime import datetime
from typing import Annotated, List

from fastapi import Depends, HTTPException
from sqlalchemy import text

import models
from dependencies import Account
from dtos.classifications import CreateClassificationReq
from dtos.expenses import CreateExpenseReq
from models import Db
from services.base import BaseService


class ExpenseService(BaseService):
    def __init__(self, db: Db):
        super(ExpenseService, self).__init__(db)

    def get_all_expenses_by_classification(self, classification_id):
        return self.db.query(models.Expenses).filter(
            models.Expenses.expense_classifications_id == classification_id).all()

    def create_expense(self, classification_id, account: Account, req: CreateExpenseReq) -> models.Expenses:
        c = models.Expenses(**req.model_dump())
        c.expense_classifications_id = classification_id
        if account is None:
            c.users_id = None
        else:
            c.users_id = account.id
        c.transaction_dt = datetime.now()
        self.db.add(c)
        self.db.commit()

        return c

    def get_expense(self, _id) -> models.Expenses:
        return self._get_by_id(_id)

    def get_expenses_by_year_month(self, year: int, month: int) -> List[models.Expenses]:
        expenses = self.db.execute(text('SELECT e.id, amount AS amount, ec.expense_type, e.transaction_dt, ec.name FROM expenses AS e '
                                        'INNER JOIN expense_classifications AS ec ON e.expense_classifications_id = ec.id '
                                        'WHERE MONTH(e.transaction_dt) = :month AND YEAR(e.transaction_dt) = :year ORDER BY e.transaction_dt ASC;'),
                                   {'month': month, 'year': year})
        return expenses.mappings().all()


    def get_grouped_expenses_by_year_month_type(self, year: int, month: int):
        expenses = self.db.execute(text('SELECT SUM(amount) AS amount, ec.expense_type FROM expenses AS e '
                                        'INNER JOIN expense_classifications AS ec ON e.expense_classifications_id = ec.id '
                                        'WHERE MONTH(e.transaction_dt) = :month AND YEAR(e.transaction_dt) = :year GROUP BY ec.expense_type ORDER BY ec.expense_type ASC;'), {'month': month, 'year': year})

        data = expenses.mappings().all()

        return data

    def _get_by_id(self, _id):
        c = self.db.query(models.Expenses).filter_by(id=_id).first()
        if c is None:
            raise HTTPException(status_code=404, detail="Expense not found")
        return c

    def edit_expense(self, expense_id: int,
                     req: CreateExpenseReq) -> models.Expenses:
        expense = self._get_by_id(expense_id)
        expense.amount = req.amount

        self.db.commit()

        return expense

    def delete_expense(self, expense_id: int) -> bool:
        c = self._get_by_id(expense_id)
        self.db.delete(c)
        self.db.commit()

        return True


def get_expense_service(db: Db):
    return ExpenseService(db)


Expense = Annotated[ExpenseService, Depends(get_expense_service)]
