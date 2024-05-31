from pydantic import BaseModel


class LoginReq(BaseModel):
    username: str
    password: str


class LoginRes(BaseModel):
    access_token: str


class RegisterRes(BaseModel):
    id: int
    username: str
