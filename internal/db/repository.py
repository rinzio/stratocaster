import os
from datetime import datetime
from typing import Dict, List, Optional

from pymongo.collection import Collection, ReturnDocument
from bson import ObjectId

from .connection import Connection
from .models import UserCollection


class Repository:

    def __init__(self) -> None:
        self._db = Connection(os.environ["MONGO_URI"], os.environ["MONGO_DB"]).db

    @property
    def users(self) -> Collection:
        return self._db["users"]

    def insert_user(self, data: Dict) -> Optional[Dict]:
        neo = self.users.insert_one(data)
        return self.get_user(neo.inserted_id)

    def get_user(self, id: str, is_active: bool = True) -> Optional[Dict]:
        return self.users.find_one({"_id": ObjectId(id), "is_active": is_active})

    def get_users(self, queryset: Optional[Dict] = None, limit: int = 1000) -> UserCollection:
        if not queryset:
            queryset = {"is_active": True}
        return UserCollection(users=self.users.find(queryset).to_list(limit))

    def soft_delete_user(self, id: str) -> Optional[Dict]:
        changeset = {
            "updated_at": datetime.now(),
            "is_active": False
        }
        return self.update_user(id, changeset)

    def update_user(self, id: str, changeset: Dict) -> Optional[Dict]:
        changeset["updated_at"] = datetime.now()
        if changeset:
            update_result = self.users.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": changeset},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return update_result
        return self.get_user(id)


REPO = Repository()
