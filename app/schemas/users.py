from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class scientometricEnum(str, Enum):
    scopus = "scopus"
    wos = "wos"
    rics = "rics"


# Shared properties
class UserBase(BaseModel):
    full_name: str = None
    scientometric_database: scientometricEnum
    document_count: int = None
    citation_count: int = None
    h_index: int = None
    url: str = None


class UserCreate(UserBase):
    document_count: int = 0
    citation_count: int = 0
    h_index: int = 0


class UserUpdate(UserBase):
    user_id: str
    full_name: str = None
    scientometric_database: scientometricEnum = None
    document_count: int = None
    citation_count: int = None
    h_index: int = None
    url: str = None


class UserInDBBase(UserBase):
    id: UUID

    class Config:
        orm_mode = True


# Дополнительные свойства для возврата через API
class User(UserInDBBase):
    pass


# Дополнительные свойства, хранящиеся в БД
class UserInDB(UserInDBBase):
    pass
