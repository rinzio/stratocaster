import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import EmailStr
from pymongo.collection import Collection, ReturnDocument
from bson import ObjectId

from .repository import Repository

from ..models import PatientModel
from ..connection import Connection
from ...env import MONGO_DB, MONGO_URI


_conn = Connection(MONGO_URI, MONGO_DB)
if _conn is None:
    raise RuntimeError("Connection to DB could not be established")


class PatientRepo(Repository):

    __sui: Collection = _conn.db["patients"] # type: ignore

    @classmethod
    def create(cls, data: Dict) -> PatientModel:
        neo = cls.__sui.insert_one(data)
        return PatientModel.model_validate(cls.get(neo.inserted_id))

    @classmethod
    def get(cls, id: str | None = None, email: EmailStr | None = None, is_active: bool = True) -> Optional[PatientModel]:
        query: Dict[str, Any] = {"is_active": is_active}
        if id is not None:
            query["_id"] = ObjectId(id)
        if email is not None:
            query["email"] = email
    
        if (data := cls.__sui.find_one(query)):
            return PatientModel.model_validate(data)

    @classmethod
    def list(cls, queryset: Optional[Dict[str, Any]] = None, limit: int = 1000) -> List[PatientModel]:
        if not queryset:
            queryset = {"is_active": True}
        data = cls.__sui.find(queryset).to_list(limit)
        return [PatientModel.model_validate(obj) for obj in data]

    @classmethod
    def delete(cls, id: str | None = None, email: EmailStr | None = None, soft: bool = True) -> Optional[PatientModel]:
        if soft:
            changeset = {
                "updated_at": datetime.now(),
                "is_active": False
            }
            return cls.update(id, email, changeset=changeset)
        raise RuntimeError(f"Hard delete not defined for patients")

    @classmethod
    def update(cls, id: str | None = None, email: EmailStr | None = None, changeset: Dict = {}) -> Optional[PatientModel]:
        changeset["updated_at"] = datetime.now()
        query: Dict[str, Any] = {"is_active": True} # Only active patients can be updated
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
                return PatientModel.model_validate(update_result)
        return cls.get(id, email)
