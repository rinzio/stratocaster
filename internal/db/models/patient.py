from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from .id_ import PyObjectId


class PatientModel(BaseModel):
    # ID
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # Required fields
    name: str
    email: EmailStr  # TODO: Unique constraint
    p_lastname: str

    # Optional fields
    m_lastname: Optional[str] = None
    birthdate: Optional[datetime] = None

    # Timestamps
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # Flags
    is_active: bool = True
    is_new: bool = True


class PatientChangeset(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str]
    email: Optional[EmailStr]
    p_lastname: Optional[str]
    m_lastname: Optional[str]
    birthdate: Optional[datetime]
