from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from .id_ import PyObjectId


class User(BaseModel):
    # ID
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # Required fields
    name: str
    email: EmailStr
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


class UserCollection(BaseModel):
    """
    A container holding a list of `User` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    users: List[User]


class UpdateUserChangesetModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str]
    email: Optional[EmailStr]
    p_lastname: Optional[str]
    m_lastname: Optional[str]
    birthdate: Optional[datetime]
