from fastapi import APIRouter

from dependencies import Account
from dtos.auth import LoginReq, LoginRes, RegisterRes, GetAccountRes
from services.auth import Auth

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['auth']
)

@router.get('/account')
async def get_account(account: Account) -> GetAccountRes:
    """Sisäänkirjautunut käyttäjä"""

    return account



@router.post('/login')
async def login(req: LoginReq, service: Auth) -> LoginRes:
    """ Sisäänkirjautuminen """

    access_token = service.login(req.username, req.password)

    return LoginRes(access_token=access_token)


@router.post('/logout')
async def logout(account: Account, service: Auth):
    """ Uloskirjautuminen """
    service.logout(account)
    return ""

@router.post('/register')
async def login(req: LoginReq, service: Auth) -> RegisterRes:
    """ Uuden käyttäjän lisääminen """

    user = service.create_user(req)
    return user
