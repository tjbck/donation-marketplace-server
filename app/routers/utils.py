from fastapi import APIRouter
from pydantic import BaseModel

from app.internal.utils import verify_password, get_password_hash
from app.libs.geolocation import get_address_from_location
from app.libs.recaptcha import verify_recaptcha
from app.libs.spam import detect_spam

import requests
import uuid
import config

router = APIRouter()


###############################
# Verify Recaptcha
###############################

@router.get("/utils/recaptcha", tags=["utils"])
async def check_recaptcha_token(token: str = ""):
    print(token)
    return {"status": verify_recaptcha(token)}

###############################
# Get Geolocation Data
###############################


@router.get("/utils/geolocation", tags=["utils"])
async def get_address(lat: str = "", lon: str = ""):
    return get_address_from_location(lat, lon)

###############################
# Get Spam Status
###############################


@router.get("/utils/spam", tags=["utils"])
async def check_spam(text: str = ""):
    print(text)
    return {"spam": detect_spam(text)}

###############################
# Get Hashed String
###############################


@router.get("/utils/hash", tags=["utils"])
async def get_hashed_value(value: str = ""):
    return {"value": value, "hashed": get_password_hash(value)}

###############################
# Get UUID4 String
###############################


@router.get("/utils/uuid", tags=["utils"])
async def get_uuid():
    return {"value": str(uuid.uuid4())}
