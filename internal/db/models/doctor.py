from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from internal.db.models.user import BaseUserModel

from .id_ import PyObjectId


class DoctorModel(BaseUserModel):
    # Profesional
    profesional_id: str
    university: str  # TODO: Use an enum instead of string

    # Relationships
    patients: List[PyObjectId] = []
    speciality: Optional[str] = "General"  # TODO: Use an enum instead of string, use a list


class DoctorChangeset(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None 
    p_lastname: Optional[str] = None
    m_lastname: Optional[str] = None
    birthdate: Optional[datetime] = None
    speciality: Optional[str] = None
    university: Optional[str] = None



class DoctorPatientsChangeset(BaseModel):
    patients: List[PyObjectId]
