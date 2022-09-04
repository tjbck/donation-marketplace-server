from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel

from app.internal.constants import ERROR_MESSAGES
from app.libs.recaptcha import verify_recaptcha
from app.internal.utils import bearer_scheme
from app.models.reviews import ReviewModel, Reviews
from app.models.users import UserModel, Users

import requests
import uuid
import time
import config

router = APIRouter()

###############################
# Forms
###############################


class ReviewForm(BaseModel):
    user_id: str
    rating: int
    content: str


class ReviewsResponse(BaseModel):
    reviews: List[ReviewModel]
    users: List[UserModel]


###############################
# Get User Reviews
###############################

@router.get("/reviews/{user_id}", response_model=ReviewsResponse, tags=["reviews"])
async def get_reviews(user_id: str):
    reviews = Reviews.get_reviews_by_user_id(user_id)
    users = Users.get_users_by_ids([review.reviewer_id for review in reviews])

    return {
        "reviews": reviews,
        "users": users
    }


###############################
# Add User Review
###############################

@router.post("/reviews/add", response_model=ReviewModel, tags=["reviews"])
async def post_review(form_data: ReviewForm, cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = cred.credentials
    reviewer = Users.get_user_by_token(token)
    if (reviewer):
        review = Reviews.insert_review(
            form_data.user_id, reviewer.id, form_data.rating, form_data.content)
        return review
    else:
        raise HTTPException(400, ERROR_MESSAGES['INVALID_CRED'])
