
from pydantic import BaseModel
from typing import List, Union
from pymongo import ReturnDocument
import time
import uuid
import config


DB = config.db

#####################
# Model
#####################


class MessageUserModel(BaseModel):
    id: str
    name: str


class MessageModel(BaseModel):
    content: str
    user: MessageUserModel


class ChatModel(BaseModel):
    id: str
    user_ids: List[str]
    messages: List[MessageModel] = []
    updatedAt: int = int(time.time())  # Epoch Time

#####################
# Table
#####################


class ChatsTable:
    def __init__(self, db):
        self.db = db
        self.collection = db.chats

    def insert_chat(self, user_ids: List[str]) -> Union[None, ChatModel]:
        user_ids = sorted(user_ids)
        chat = ChatModel(**{
            "id": '#'.join(user_ids),
            "user_ids": user_ids,
        })

        result = self.collection.insert_one(chat.dict())
        return chat if result.acknowledged else None

    def get_chats_by_user_id(self, user_id: str) -> List[ChatModel]:
        chats = list(self.collection.find(
            {"user_ids": {'$in': [user_id]}}, {"_id": False}).sort('updatedAt', -1))

        return [ChatModel(**chat) for chat in chats]

    def get_chat_by_user_ids(self, user_ids: List[str]) -> Union[None, ChatModel]:
        user_ids = sorted(user_ids)
        chat = self.collection.find_one(
            {"id": '#'.join(user_ids)}, {"_id": False})
        return ChatModel(**chat) if chat else None

    def add_chat_message_by_user_ids(self, user_ids: List[str], message: MessageModel) -> Union[None, ChatModel]:
        user_ids = sorted(user_ids)
        chat = self.collection.find_one_and_update(
            {"id": '#'.join(user_ids)}, {'$push': {'messages': message.dict()}, '$set': {'updatedAt': int(time.time())}}, {'_id': False}, return_document=ReturnDocument.AFTER)
        return ChatModel(**chat) if chat else None


Chats = ChatsTable(DB)
