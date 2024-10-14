import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from pymongo.collection import Collection, ReturnDocument
from bson import ObjectId

from .repository import Repository

from ..models import PatientModel
from ..connection import Connection
from ..env import MONGO_DB, MONGO_URI


_conn = Connection(MONGO_URI, MONGO_DB).db
if _conn is None:
    raise RuntimeError("Connection to DB could not be established")


class Patients(Repository):

    __sui: Collection = _conn.db["patients"]

    @classmethod
    def create(cls, data: Dict) -> PatientModel:
        neo = cls.__sui.insert_one(data)
        return PatientModel.parse_obj(cls.get(neo.inserted_id))

    @classmethod
    def get(cls, id: str, is_active: bool = True) -> Optional[PatientModel]:
        if (data := cls.__sui.find_one({"_id": ObjectId(id), "is_active": is_active})):
            return PatientModel.parse_obj(data)

    @classmethod
    def list(cls, queryset: Optional[Dict[str, Any]] = None, limit: int = 1000) -> List[PatientModel]:
        if not queryset:
            queryset = {"is_active": True}
        data = cls.__sui.find(queryset).to_list(limit)
        return [PatientModel.parse_obj(obj) for obj in data]

    @classmethod
    def delete(cls, id: str, soft: bool = True) -> Optional[PatientModel]:
        if soft:
            changeset = {
                "updated_at": datetime.now(),
                "is_active": False
            }
            return cls.update(id, changeset)
        raise RuntimeError(f"Hard delete not defined for patients")

    @classmethod
    def update(cls, id: str, changeset: Dict) -> Optional[PatientModel]:
        changeset["updated_at"] = datetime.now()
        if changeset:
            update_result = cls.__sui.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": changeset},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return PatientModel.parse_obj(update_result)
        return cls.get(id)
