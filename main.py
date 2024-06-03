from fastapi import FastAPI
from sqlalchemy.sql.functions import user

from controllers import auth, expense_classifications

app = FastAPI()

app.include_router(auth.router)
app.include_router(expense_classifications.router)