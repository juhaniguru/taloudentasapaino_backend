from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException

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

    def create_expense(self, classification_id, account: Account,  req: CreateExpenseReq) -> models.Expenses:
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
