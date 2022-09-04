from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel

from app.internal.constants import ERROR_MESSAGES
from app.internal.utils import bearer_scheme
from app.libs.file import save_file
from app.libs.recaptcha import verify_recaptcha
from app.libs.spam import detect_spam
from app.models.users import Users
from app.models.listings import ListingItemModel, Listings

import requests
import uuid
import time
import config

router = APIRouter()


###############################
# Forms
###############################


class AddItemForm(BaseModel):
    recaptcha_token: str
    title: str
    content: str


class UpdateItemAvailabilityForm(BaseModel):
    item_id: str
    availability: bool


###############################
# Get New Items (Last 4)
###############################

@router.get("/listings/new", response_model=List[ListingItemModel], tags=["listings"])
async def get_new_listings(limit: Optional[int] = 4):
    items = Listings.get_items(limit=limit)
    return items

###############################
# Get Items
###############################


@router.get("/listings", response_model=List[ListingItemModel], tags=["listings"])
async def get_listings(query: Optional[str] = None, cursor: Optional[int] = 0, limit: Optional[int] = 8):
    items = Listings.get_items(query, cursor, limit)
    print(items)
    return items

###############################
# Add Listing Item
###############################


@router.post("/listings/add", tags=["listings"])
async def post_listings(file: UploadFile, recaptcha_token: str = Form(), title: str = Form(), content: str = Form(), cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials
    if(verify_recaptcha(recaptcha_token)):
        user = Users.get_user_by_token(token)
        if(user):
            if(not detect_spam(content)):
                filename = await save_file(file)
                item = Listings.insert_item(user, title, content, filename)
                return item
            else:
                raise HTTPException(
                    401, detail=ERROR_MESSAGES['SPAM'])
        else:
            raise HTTPException(
                401, detail=ERROR_MESSAGES['INVALID_CRED'])
    else:
        raise HTTPException(
            500, detail=ERROR_MESSAGES['BOT'])

###############################
# Get User Items
###############################


@router.get("/listings/users/{user_id}", tags=["listings"])
async def get_user_items(user_id: str):
    user = Users.get_user_by_id(user_id)
    if(user):
        items = Listings.get_items_by_user_id(user_id)
        return {
            "items": items,
            "user": user
        }
    else:
        raise HTTPException(
            500, detail=ERROR_MESSAGES['USER_NOT_FOUND'])


###############################
# Get Item Info
###############################


@router.get("/listings/items/{item_id}", tags=["listings"])
async def get_item_info(item_id: str):
    item = Listings.get_item_by_id(item_id)

    if(item):
        user = Users.get_user_by_id(item.user_id)

        if(user):
            return {
                "item": item,
                "user": user
            }
        else:
            raise HTTPException(
                500, detail=ERROR_MESSAGES['USER_NOT_FOUND'])
    else:
        raise HTTPException(
            500, detail=ERROR_MESSAGES['ITEM_NOT_FOUND'])


###############################
# Update Item Availability
###############################


@router.post("/listings/items/edit/availability", tags=["listings"])
async def update_item_availability(form_data: UpdateItemAvailabilityForm, cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials
    user = Users.get_user_by_token(token)

    if(user):
        item = Listings.update_item_availability_by_id(
            form_data.item_id, form_data.availability)

        if(item):
            return item
        else:
            raise HTTPException(
                500, detail=ERROR_MESSAGES['ITEM_NOT_FOUND'])
    else:
        raise HTTPException(
            500, detail=ERROR_MESSAGES['USER_NOT_FOUND'])
