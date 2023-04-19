import enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, AnyUrl, constr, validator

list_filds = ['documents', 'citations']


class scientometric_status(enum.Enum):
    scopus = "scopus"
    wos = "wos"
    risc = "risc"


# Shared properties
class UserBase(BaseModel):
    guid: UUID = None
    full_name: constr(strip_whitespace=True)
    scientometric_database: scientometric_status
    document_count: int
    citation_count: int
    h_index: int
    url: AnyUrl
    created_at: Optional[int] = None

    @validator('full_name')
    def check_alpha(cls, v):
        l = v.split()
        if len(l) < 3:
            raise ValueError('Must be 3 or more words')
        for i in l:
            if not i.isalpha():
                raise ValueError('Name must contain only alphabetical characters')

        return v.title()

    @validator('document_count', 'citation_count', 'h_index')
    def check_plus(cls, v):
        if v < 0:
            raise ValueError(f'document_count,citation_count,h_index must be greater than or equal to 0')
        return v


class TestUserGet(BaseModel):
    full_name: str
    h_index: int
    url: AnyUrl
    document_count: Optional[int] = None
    citation_count: Optional[int] = None

    class Config:
        orm_mode = True


class UserGet(BaseModel):
    full_name: str
    h_index: int
    url: AnyUrl

    class Config:
        orm_mode = True


class ProfilesGet(BaseModel):
    filter: scientometric_status
    page: int = 1
    page_size: int = 10
    sort_hirsch: str = "up"
    sort_time: str = "up"

    @validator('page_size')
    def check_max(cls, v):
        if v > 10:
            raise ValueError(f'page_size must not be greater than 10')
        return v

    @validator('page', 'page_size')
    def check_plus(cls, v):
        if v < 0:
            raise ValueError(f'page and page_size must be greater than or equal to 0')
        return v

    @validator('sort_hirsch', 'sort_time')
    def check_alpha(cls, v):
        if not v.isalpha():
            raise ValueError('Name must contain only alphabetical characters')
        return v

    @validator('sort_hirsch', 'sort_time')
    def check_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('Must be a string')
        if v != 'up' and v != 'down':
            raise ValueError('up or down')
        return v

    class Config:
        orm_mode = True


class ProfileGet(BaseModel):
    guid: UUID
    scientometric_database: scientometric_status
    fields: Optional[list[str]] = None

    @validator('fields')
    def check_list_fields(cls, v):
        for i in v:
            if i not in list_filds:
                raise ValueError('There are no such additional fields')
        return v

    class Config:
        orm_mode = True


class StatGet(BaseModel):
    scientometric_database: scientometric_status
    documents_sum: int
    citations_sum: int
    average_h_index: float

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    document_count: int = 0
    citation_count: int = 0
    h_index: int = 0


class UserUpdate(UserBase):
    guid: UUID
    full_name: str
    scientometric_database: scientometric_status
    document_count: int = None
    citation_count: int = None
    h_index: int = None
    url: AnyUrl = None


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
