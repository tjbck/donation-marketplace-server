from fastapi.security import HTTPBasicCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
import jwt
import config

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

############################
# Authentication Utils
############################

bearer_scheme = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) if hashed_password else False


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: Union[timedelta, None] = None):
    payload = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
