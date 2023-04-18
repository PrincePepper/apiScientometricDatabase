from typing import Generator, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel

from app.db.session import SessionLocal


def get_db() -> Generator:
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()


class UserNotFound(Exception):
    pass


schemas = TypeVar("schemas", bound=BaseModel)


class BaseGenericResponse(GenericModel, Generic[schemas]):
    status: int = 0
    message: str = "ok"
    data: schemas
