from pydantic import BaseModel
from typing import List, Union
import uuid
import config

from app.libs.token import decodeToken

DB = config.db

#####################
# Model
#####################


class AuthModel(BaseModel):
    id: str
    email: str
    password: str
    active: bool = True

#####################
# Table
#####################


class AuthsTable:
    def __init__(self, db):
        self.db = db

    def insert_auth(self, id: str, email: str, password: str) -> Union[None, AuthModel]:
        auth = AuthModel(**{
            "id": id,
            "email": email,
            "password": password
        })

        print(auth.dict())
        result = self.db.auths.insert_one(auth.dict())

        return auth if result.acknowledged else None

    def get_auth_by_token(self, token: str) -> Union[None, AuthModel]:
        payload = decodeToken(token)
        print(payload['email'])

        return self.get_auth_by_email(payload['email'])

    def get_auth_by_email(self, email: str) -> Union[None, AuthModel]:
        auth = self.db.auths.find_one(
            {"email": email}, {'_id': False})
        print(auth)
        return AuthModel(**auth) if auth else None


Auths = AuthsTable(DB)
