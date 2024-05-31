from fastapi import FastAPI
from sqlalchemy.sql.functions import user

from controllers import auth

app = FastAPI()

app.include_router(auth.router)