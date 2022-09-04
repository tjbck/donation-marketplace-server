from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from typing import List, Optional
from pydantic import BaseModel

from app.internal.constants import ERROR_MESSAGES
from app.libs.recaptcha import verify_recaptcha
from app.internal.utils import bearer_scheme
from app.models.reviews import ReviewModel, Reviews
from app.models.users import UserModel, Users
from app.models.chats import Chats


import requests
import uuid
import time
import config

router = APIRouter()

###############################
# All Chats
###############################


@router.get("/chats", tags=["chats"])
async def get_chats(cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials
    user = Users.get_user_by_token(token)
    chats = Chats.get_chats_by_user_id(user.id)

    user_ids = []
    for chat in chats:
        user_ids.extend(
            [user_id for user_id in chat.user_ids if user_id != user.id])
    user_ids = list(set(user_ids))

    print(user_ids)

    users = Users.get_users_by_ids(user_ids)

    return {
        "chats": chats,
        "users": users
    }

###############################
# User Chat
###############################


@router.get("/chats/{user_id}", tags=["chats"])
async def get_chats(user_id: str, cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials
    user = Users.get_user_by_token(token)
    chat = Chats.get_chat_by_user_ids([user_id, user.id])

    if chat == None:
        chat = Chats.insert_chat([user_id, user.id])

    return chat
