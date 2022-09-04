from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from typing import Union, List
from pydantic import BaseModel

from app.internal.utils import verify_password, get_password_hash, bearer_scheme
from app.internal.constants import ERROR_MESSAGES
from app.models.users import UserModel, Users
from app.libs.token import decodeToken

import time
import config

router = APIRouter()

###############################
# Form
###############################


class UserUpdateForm(BaseModel):
    name: Union[str, None] = None
    mobile: Union[str, None] = None
    address: Union[str, None] = None
    coords: Union[List[str], None] = None

###############################
# Get Session User
###############################


@router.get("/users/me", tags=["users"])
async def get_session_user_info(cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials
    user = Users.get_user_by_token(token)
    if(user):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials")

###############################
# Get User by User Id
###############################


@router.get("/users/{user_id}", tags=["users"])
async def get_user_by_id(user_id: str):
    user = Users.get_user_by_id(user_id)
    if(user):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES['DEFAULT'])


###############################
# Update Session User Info
###############################


@router.post("/users/update", tags=["users"])
async def update_session_user_info(form_data: UserUpdateForm, cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials
    user = Users.get_user_by_token(token)

    if(user):
        updated_user = Users.update_user_by_id(
            user.id, form_data.dict(exclude_none=True))
        return updated_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials")
