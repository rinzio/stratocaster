from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import EmailStr
from pymongo.collection import Collection, ReturnDocument
from bson import ObjectId

from internal.db.models.id_ import PyObjectId

from .repository import Repository

from ..models import BaseUserModel
from ..connection import Connection
from ...env import MONGO_DB, MONGO_URI


_conn = Connection(MONGO_URI, MONGO_DB).db
if _conn is None:
    raise RuntimeError("Connection to DB could not be established")


class UserRepo(Repository):

    __sui: Collection = _conn.db["users"]

    @classmethod
    def create(cls, data: Dict) -> BaseUserModel:
        neo = cls.__sui.insert_one(data)
        return BaseUserModel.model_validate(cls.get(neo.inserted_id))

    @classmethod
    def get(cls, id: str | None = None, email: EmailStr | None = None, is_active: bool = True) -> Optional[BaseUserModel]:
        query: Dict[str, Any] = {"is_active": is_active}
        if id is not None:
            query["_id"] = ObjectId(id)
        if email is not None:
            query["email"] = email
    
        if (data := cls.__sui.find_one(query)):
            return BaseUserModel.model_validate(data)

    @classmethod
    def list(cls, queryset: Optional[Dict[str, Any]] = None, limit: int = 1000) -> List[BaseUserModel]:
        if not queryset:
            queryset = {"is_active": True}
        data = cls.__sui.find(queryset).to_list(limit)
        return [BaseUserModel.model_validate(obj) for obj in data]

    @classmethod
    def delete(cls, id: str | None = None, email: EmailStr | None = None, soft: bool = True) -> Optional[BaseUserModel]:
        if soft:
            changeset = {
                "updated_at": datetime.now(),
                "is_active": False
            }
            return cls.update(id, email, changeset)
        raise RuntimeError(f"Hard delete not defined for doctors")

    @classmethod
    def update(cls, id: str | None = None, email: EmailStr | None = None, changeset: Dict = {}) -> Optional[BaseUserModel]:
        changeset["updated_at"] = datetime.now()
        query: Dict[str, Any] = {"is_active": True} # Only active users can be updated
        if id is not None:
            query["_id"] = ObjectId(id)
        if email is not None:
            query["email"] = email
        
        if changeset:
            update_result = cls.__sui.find_one_and_update(
                query,
                {"$set": changeset},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return BaseUserModel.model_validate(update_result)
        return cls.get(id, email)
