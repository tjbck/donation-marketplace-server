from fastapi import APIRouter
from fastapi import Response
from fastapi import Cookie
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Union
from app.internal.constants import ERROR_MESSAGES

from app.internal.utils import verify_password, get_password_hash, bearer_scheme, create_token
from app.libs.recaptcha import verify_recaptcha
from app.libs.token import decodeToken
from app.models.auths import AuthModel, Auths
from app.models.users import UserModel, Users

from datetime import datetime, timedelta
import jwt
import time
import uuid
import config

router = APIRouter()

###############################
# Forms
###############################


class Token(BaseModel):
    token: str
    token_type: str


class UserBasicInfo(Token):
    email: str
    name: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class LoginForm(BaseModel):
    recaptcha_token: str
    email: str
    password: str


class RegisterForm(LoginForm):
    name: str
    mobile: str
    address: str
    coords: List[str]


###############################
# Register
###############################


@router.post("/signup",  response_model=UserBasicInfo,  tags=["auth"])
async def signup(form_data: RegisterForm, response: Response):
    if(verify_recaptcha(form_data.recaptcha_token)):
        if not Users.get_user_by_email(form_data.email.lower()):
            try:
                hashed = get_password_hash(form_data.password)
                print(form_data)

                user_id = str(uuid.uuid4())

                user = Users.insert_auth_and_user(**{
                    "id": user_id,
                    "email": form_data.email.lower(),
                    "password": hashed,
                    "name": form_data.name,
                    "mobile": form_data.mobile,
                    "address": form_data.address,
                    "coords": form_data.coords
                })

                token = create_token(data={"email": user.email})

                return {
                    "token": token,
                    "token_type": "bearer",
                    "email": user.email,
                    "name": user.name
                }

            except Exception as err:
                print(err)
                raise HTTPException(
                    500, detail=ERROR_MESSAGES['DEFAULT'])
        else:
            raise HTTPException(
                400, detail=ERROR_MESSAGES['EMAIL_TAKEN'])
    else:
        raise HTTPException(
            500, detail=ERROR_MESSAGES['BOT'])

###############################
# Login
###############################


@router.post("/login", response_model=UserBasicInfo,  tags=["auth"])
async def login(form_data: LoginForm, response: Response):

    if(verify_recaptcha(form_data.recaptcha_token)):
        user = Users.authenticate_user(form_data.email, form_data.password)
        if user:
            token = create_token(data={"email": user.email})

            return {"token": token, "token_type": "bearer", "email": user.email, "name": user.name}
        else:
            raise HTTPException(
                400, detail=ERROR_MESSAGES['LOGIN_ERROR'])
    else:
        raise HTTPException(
            500, detail=ERROR_MESSAGES['BOT'])

###############################
# Auth
###############################


@router.get("/auth",  tags=["auth"])
async def get_session_user(cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials

    auth = Auths.get_auth_by_token(token)
    user = Users.get_user_by_id(auth.id)

    if(auth):
        return {
            "email": auth.email,
            **user.dict()
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES['INVALID_CRED'])
