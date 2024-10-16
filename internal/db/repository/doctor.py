import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pymongo.collection import Collection, ReturnDocument
from bson import ObjectId

from internal.db.models.id_ import PyObjectId
from internal.db.models.patient import PatientModel

from .repository import Repository
from .patient import Patients

from ..models import DoctorModel
from ..connection import Connection
from ..env import MONGO_DB, MONGO_URI


_conn = Connection(MONGO_URI, MONGO_DB).db
if _conn is None:
    raise RuntimeError("Connection to DB could not be established")


class Doctors(Repository):

    __sui: Collection = _conn.db["doctors"]

    @classmethod
    def create(cls, data: Dict) -> DoctorModel:
        neo = cls.__sui.insert_one(data)
        return DoctorModel.model_validate(cls.get(neo.inserted_id))

    @classmethod
    def get(cls, id: str, is_active: bool = True) -> Optional[DoctorModel]:
        if (data := cls.__sui.find_one({"_id": ObjectId(id), "is_active": is_active})):
            return DoctorModel.model_validate(data)

    @classmethod
    def list(cls, queryset: Optional[Dict[str, Any]] = None, limit: int = 1000) -> List[DoctorModel]:
        if not queryset:
            queryset = {"is_active": True}
        data = cls.__sui.find(queryset).to_list(limit)
        return [DoctorModel.model_validate(obj) for obj in data]

    @classmethod
    def delete(cls, id: str, soft: bool = True) -> Optional[DoctorModel]:
        if soft:
            changeset = {
                "updated_at": datetime.now(),
                "is_active": False
            }
            return cls.update(id, changeset)
        raise RuntimeError(f"Hard delete not defined for doctors")

    @classmethod
    def update(cls, id: str, changeset: Dict) -> Optional[DoctorModel]:
        changeset["updated_at"] = datetime.now()
        if changeset:
            update_result = cls.__sui.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": changeset},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return DoctorModel.model_validate(update_result)
        return cls.get(id)

    @classmethod
    def add_patients(cls, _id: str, patients: List[PyObjectId])  -> Optional[DoctorModel]:
        doctor = cls.get(_id)
        if doctor is None:
            raise RuntimeError(f"Doctor not found {_id}")

        for patient_id in patients:
            patient = Patients.get(patient_id)
            if patient is not None and patient_id not in doctor.patients:
                doctor.patients.append(patient_id)

        return cls.update(_id, {"patients": doctor.patients})

    @classmethod
    def get_patients(
        cls,
        _id: str,
        queryset: Optional[Dict[str, Any]] = None,
        limit: int = 1000
    ) -> List[PatientModel]:
        doctor = cls.get(_id)
        if doctor is None:
            raise RuntimeError(f"Doctor not found {_id}")

        if queryset is None:
            queryset = {
                "_id": {"$in": [ObjectId(patient) for patient in doctor.patients]}
            }
        else:
            queryset["_id"] = {"$in": [ObjectId(patient) for patient in doctor.patients]}

        return Patients.list(queryset, limit)


    @classmethod
    def remove_patients(cls, _id: str, patients: List[PyObjectId])  -> Optional[DoctorModel]:
        doctor = cls.get(_id)
        if doctor is None:
            raise RuntimeError(f"Doctor not found {_id}")

        for patient_id in patients:
            patient = Patients.get(patient_id)
            if patient is not None and patient_id in doctor.patients:
                doctor.patients.remove(patient_id)

        return cls.update(_id, {"patients": doctor.patients})

    @classmethod
    def get_patient_stats(cls, _id: str) -> Dict[str, int]:
        all_ = cls.get_patients(_id)


        return {
            "masc": len([p for p in all_ if p.genre == "M"]),
            "fem": len([p for p in all_ if p.genre == "F"]),
            "total": len(all_),
        }