import os
from typing import Annotated, Optional

import jwt
from fastapi import Header, HTTPException, Depends

import models
from services.auth import Auth


def optional_login(service: Auth, authorization: object = Header(None, alias='api_key')) -> object:

    if authorization is None or authorization == "":
        return None

    header_parts = authorization.split(' ')
    if len(header_parts) != 2:
        raise HTTPException(detail='Unauthorized', status_code=401)

    if header_parts[0] != 'Bearer':
        raise HTTPException(detail='Unauthorized', status_code=401)
    decoded = jwt.decode(header_parts[1], os.getenv('SECRET'), algorithms=['HS256'])
    user = service.get_account(sub=decoded['sub'])
    if user is None:
        raise HTTPException(detail='Unauthorized', status_code=401)
    return user


def require_logged_in_user(service: Auth, authorization=Header(alias='api_key')):
    
    if authorization is None:
        raise HTTPException(detail='Unauthorized', status_code=401)

    header_parts = authorization.split(' ')

    if len(header_parts) != 2:
        raise HTTPException(detail='Unauthorized', status_code=401)

    if header_parts[0] != 'Bearer':
        raise HTTPException(detail='Unauthorized', status_code=401)

    decoded = jwt.decode(header_parts[1], os.getenv('SECRET'), algorithms=['HS256'])
    user = service.get_account(sub=decoded['sub'])
    if user is None:
        raise HTTPException(detail='Unauthorized', status_code=401)
    return user


Account = Annotated[models.Users, Depends(require_logged_in_user)]
OptionalAccount = Annotated[Optional[models.Users], Depends(optional_login)]
