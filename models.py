import os
from typing import List, Optional, Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Index, Integer, String, create_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship, sessionmaker, Session
from sqlalchemy.orm.base import Mapped

Base = declarative_base()

load_dotenv()

engine = create_engine(os.getenv('DB'))
ses = sessionmaker(bind=engine)


class ExpenseClassifications(Base):
    __tablename__ = 'expense_classifications'
    __table_args__ = (
        Index('name_UNIQUE', 'name', unique=True),

    )

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(45), nullable=False)
    expense_type = mapped_column(String(45), nullable=False)

    expenses: Mapped[List['Expenses']] = relationship('Expenses', uselist=True, back_populates='expense_classifications')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('username_UNIQUE', 'username', unique=True),
    )

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(45), nullable=False)
    password = mapped_column(String(255), nullable=False)
    access_jti = mapped_column(String(45))

    expenses: Mapped[List['Expenses']] = relationship('Expenses', uselist=True, back_populates='users')


class Expenses(Base):
    __tablename__ = 'expenses'
    __table_args__ = (
        ForeignKeyConstraint(['expense_classifications_id'], ['expense_classifications.id'], name='fk_expenses_expense_classifications'),
        ForeignKeyConstraint(['users_id'], ['users.id'], name='fk_expenses_users1'),
        Index('fk_expenses_expense_classifications_idx', 'expense_classifications_id'),
        Index('fk_expenses_users1_idx', 'users_id')
    )

    id = mapped_column(Integer, primary_key=True)
    amount = mapped_column(Integer, nullable=False)
    transaction_dt = mapped_column(DateTime, nullable=False)
    expense_classifications_id = mapped_column(Integer, nullable=False)
    users_id = mapped_column(Integer)

    expense_classifications: Mapped['ExpenseClassifications'] = relationship('ExpenseClassifications', back_populates='expenses')
    users: Mapped[Optional['Users']] = relationship('Users', back_populates='expenses')


def get_db():
    db = ses()
    try:

        yield db

    finally:

        db.close()


Db = Annotated[Session, Depends(get_db)]