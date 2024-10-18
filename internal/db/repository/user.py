from typing import Dict

from pydantic import EmailStr
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from internal.db.models.id_ import PyObjectId

from .repository import Repository

from ..models import BaseUserModel
from ..connection import Connection
from ...env import MONGO_DB, MONGO_URI


_conn = Connection(MONGO_URI, MONGO_DB)
if _conn is None:
    raise RuntimeError("Connection to DB could not be established")


class UserRepo(Repository):

    __sui: Collection = _conn.db["users"] # type: ignore

    @classmethod
    def create(cls, data: Dict) -> BaseUserModel:
        try:
            neo = cls.__sui.insert_one(data)
            return BaseUserModel.model_validate(cls.get(neo.inserted_id))
        except DuplicateKeyError:
            raise RuntimeError("Duplicated key, user not created")
