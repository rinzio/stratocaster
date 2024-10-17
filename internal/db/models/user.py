from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, SecretStr

from .id_ import PyObjectId


class Role(int, Enum):
    ADMIN = 1
    DOCTOR = 2
    VIEWER = 3


class BaseUserModel(BaseModel):
    # ID
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    # Auth
    email: EmailStr
    password: str
    role: Role

    # Required fields
    name: str
    p_lastname: str

    # Timestamps
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # Flags
    is_active: bool = True

