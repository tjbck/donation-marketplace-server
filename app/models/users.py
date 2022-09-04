
from pydantic import BaseModel
from typing import List, Union
from pymongo import ReturnDocument
import uuid
import datetime
import time
import config

from app.internal.utils import verify_password
from app.models.auths import Auths
from app.libs.token import decodeToken


DB = config.db


#####################
# Model
#####################

class UserModel(BaseModel):
    id: str
    name: str
    mobile: str
    address: str
    coords: List[str]
    createdAt: int = int(time.time())


class UserEmailModel(UserModel):
    email: str

#####################
# Table
#####################


class UsersTable:
    def __init__(self, db):
        self.db = db

    def authenticate_user(self, email: str, password: str) -> Union[None, UserEmailModel]:
        auth = Auths.get_auth_by_email(email)
        if (auth):
            if verify_password(password, auth.password):
                user = self.get_user_by_id(auth.id)

                return UserEmailModel(**{**user.dict(), 'email': auth.email}) if user else None
            else:
                return None
        else:
            return None

    def insert_auth_and_user(self, id: str, email: str, password: str, name: str, mobile: str, address: str, coords: List[str]) -> Union[None, UserEmailModel]:
        auth = Auths.insert_auth(id, email, password)
        if(auth):
            user = self.insert_user(id, name, mobile, address, coords)
            return UserEmailModel(**{**user.dict(), 'email': auth.email}) if user else None
        else:
            return None

    def insert_user(self, id: str, name: str, mobile: str, address: str, coords: List[str]) -> Union[None, UserModel]:
        user = UserModel(**{
            "id": id,
            "name": name,
            "mobile": mobile,
            "address": address,
            "coords": coords,
            "createdAt": int(time.time()),
        })

        print(user.dict())

        result = self.db.users.insert_one(user.dict())
        return user if result.acknowledged else None

    def get_user_by_token(self, token: str) -> Union[None, UserEmailModel]:
        payload = decodeToken(token)
        print(payload['email'])

        return self.get_user_by_email(payload['email'])

    def get_user_by_email(self, email: str) -> Union[None, UserEmailModel]:
        auth = Auths.get_auth_by_email(email)
        if auth:
            user = self.get_user_by_id(auth.id)
            return UserEmailModel(**{**user.dict(), 'email': auth.email}) if user else None
        else:
            return None

    def get_user_by_id(self, id: str) -> Union[None, UserModel]:
        user = self.db.users.find_one(
            {"id": id}, {'_id': False})
        return UserModel(**user) if user else None

    def get_users_by_ids(self, ids: List[str]) -> List[UserModel]:
        users = list(self.db.users.find(
            {"id": {"$in": ids}}, {'_id': False}))
        return [UserModel(**user) for user in users]

    def update_user_by_id(self, id: str, update: dict) -> Union[None, UserModel]:
        print(id, update)
        res = self.db.users.find_one_and_update(
            {"id": id}, {"$set": update}, {'_id': False}, return_document=ReturnDocument.AFTER)
        return UserModel(**res) if res else None


Users = UsersTable(DB)
