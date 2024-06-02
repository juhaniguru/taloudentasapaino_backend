import logging
import os
from typing import Annotated

import jwt
import passlib
from fastapi import Depends, HTTPException
from passlib.hash import pbkdf2_sha512 as pl
import uuid

import models
from dtos.auht import LoginReq
from models import Db
from services.base import BaseService


class AuthService(BaseService):
    def __init__(self, db: Db):
        super(AuthService, self).__init__(db)

    def create_user(self, req: LoginReq) -> models.Users:
        try:
            user = models.Users(**req.model_dump())
            user.password = pl.hash(user.password)
            self.db.add(user)
            self.db.commit()
            return user
        except Exception as e:
            logging.exception(e)
            raise HTTPException(detail='user cannot be created', status_code=400)

    def _find_by_username(self, username: str) -> models.Users:
        user = self.db.query(models.Users).filter(models.Users.username == username).first()
        if user is None:
            raise HTTPException(detail='user not found', status_code=404)

        return user

    def _find_by_sub(self, sub):
        user = self.db.query(models.Users).filter_by(models.Users.access_jti == sub).first()
        if user is None:
            raise HTTPException(detail='user not found', status_code=404)
        return user

    def login(self, username: str, password: str) -> str:
        user = self._find_by_username(username)
        if pl.verify(password, user.password):
            access_token_sub = str(uuid.uuid4())
            access_token = jwt.encode({'sub': access_token_sub}, os.getenv('SECRET'), algorithm='HS256')
            user.access_jti = access_token_sub
            self.db.commit()
            return access_token
        raise HTTPException(detail='invalid username or password', status_code=401)

    def logout(self, user: models.Users):

        user.access_jti = ''
        self.db.commit()
        return True

    def get_account(self, sub=None, username=None):
        if sub is not None:
            user = self._find_by_sub(sub)
        elif username is not None:
            user = self._find_by_username(username)
        else:
            raise HTTPException(detail='invalid sub or username', status_code=401)
        return user


def get_auth_service(db: Db):
    return AuthService(db)


Auth = Annotated[AuthService, Depends(get_auth_service)]
