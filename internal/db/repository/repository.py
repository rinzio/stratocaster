from typing import Any, Dict, Optional, Protocol, List, TypeVar
from pymongo.collection import Collection
from pydantic import BaseModel, EmailStr


T = TypeVar("T")

class Repository(Protocol):
    __sui: Collection
    @classmethod
    def create(cls, data: Dict[str, Any]) -> BaseModel: ...
    @classmethod
    def get(cls, id: str | None = None, email: EmailStr | None = None, is_active: bool = True) -> Optional[BaseModel]: ...
    @classmethod
    def list(cls, queryset: Optional[Dict[str, Any]] = None, limit: int = 1000) -> List[T]: ...
    @classmethod
    def delete(cls, id: str | None = None, email: EmailStr | None = None, soft: bool = True) -> Optional[BaseModel]: ...
    @classmethod
    def update(cls, id: str | None = None, email: EmailStr | None = None, changeset: Dict[str, Any] = {}) -> Optional[BaseModel]: ...
