from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from bson import ObjectId

from .id_ import PyObjectId


class DoctorModel(BaseModel):
    # ID
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # Required fields
    name: str
    prof_id: str  # TODO: Add validator
    email: EmailStr # TODO: Unique constraint
    p_lastname: str

    # Relationships
    patients: List[PyObjectId] = []

    # Optional fields
    m_lastname: Optional[str] = None
    birthdate: Optional[datetime] = None
    speciality: Optional[str] = "General"

    # Timestamps
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # Flags
    is_active: bool = True


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



class DoctorPatientsChangeset(BaseModel):
    patients: List[PyObjectId]
