from typing import Optional
from pydantic import BaseModel

from auth.schemas.base import BaseRequest
from auth.schemas.base import BaseResponse
from auth.models.orm.tables import User


class SignUpRequest(BaseModel):
    email: str
    password: str

class SignUpResponse(BaseResponse):
    user: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseResponse):
    access_token: str

class LogoutRequest(BaseModel):
    access_token: str


class LogoutResponse(BaseResponse):
    message: str = "Successfully logged out ... bye"


class TokenValidateRequest(BaseModel):
    access_token: str

class TokenValidateResponse(BaseResponse):
    user_is_valid: bool

