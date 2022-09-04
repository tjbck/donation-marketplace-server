from pydantic import BaseModel
from typing import List, Optional, Union
from pymongo import ReturnDocument
import re
import time
import uuid
import config

from app.models.users import UserModel

DB = config.db

#####################
# Model
#####################


class ListingItemModel(BaseModel):
    id: str
    user_id: str

    availability: bool = True  # Item availability

    title: str
    content: str
    images: List[str]

    # We store address separately from the user data because they might move.
    address: str
    coords: List[str]  # Same applies here

    createdAt: int = int(time.time())
    updatedAt: int = int(time.time())


#####################
# Table
#####################

class ListingsTable:
    def __init__(self, db):
        self.db = db
        self.collection = db.listings

    def insert_item(self, user: UserModel, title: str, content: str, filename: str) -> Union[None, ListingItemModel]:
        item = ListingItemModel(**{
            "id": str(uuid.uuid4()),
            "user_id": user.id,

            "title": title,
            "content": content,

            "images": [f'/static/{filename}'],

            "address": user.address,
            "coords": user.coords,
        })

        result = self.collection.insert_one(item.dict())
        return item if result.acknowledged else None

    def get_item_by_id(self, id: str) -> Union[None, ListingItemModel]:
        item = self.collection.find_one(
            {"id": id}, {"_id": False})

        return ListingItemModel(**item) if item else None

    def get_items(self, query: Optional[Union[None, str]] = None, cursor: int = 0, limit: int = 50) -> List[ListingItemModel]:
        if query:
            items = list(self.collection.find(
                {"title": re.compile(query, re.IGNORECASE)}, {"_id": False}).sort('_id', -1).skip(cursor*limit).limit(limit))
        else:
            items = list(self.collection.find(
                {}, {"_id": False}).sort('_id', -1).skip(cursor*limit).limit(limit))

        return [ListingItemModel(**item) for item in items]

    def get_items_by_user_id(self, user_id: str) -> List[ListingItemModel]:
        items = list(self.collection.find(
            {"user_id": user_id}, {"_id": False}).sort('_id', -1))

        return [ListingItemModel(**item) for item in items]

    def update_item_availability_by_id(self, id: str, availability: bool) -> Union[None, ListingItemModel]:
        item = self.collection.find_one_and_update(
            {"id": id}, {"$set": {
                "availability": availability
            }},
            {'_id': False},
            return_document=ReturnDocument.AFTER)

        return ListingItemModel(**item) if item else None


Listings = ListingsTable(DB)
