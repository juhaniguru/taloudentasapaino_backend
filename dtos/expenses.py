import datetime
from typing import List, Optional

from pydantic import BaseModel

from dtos.auth import GetAccountRes


class CreateExpenseReq(BaseModel):
    amount: int


class ExpenseRes(BaseModel):
    amount: int
    transaction_dt: datetime.datetime
    users: Optional[GetAccountRes]
