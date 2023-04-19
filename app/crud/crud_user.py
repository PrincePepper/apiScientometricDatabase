from typing import Optional, Type

from sqlalchemy import func, Row
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate, StatGet


class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):

    def get_by_guid(self, db: Session, *, id: str) -> Optional[Users]:
        return db.query(Users).filter(Users.guid == id).first()

    def get_profile(self, db: Session, *, id: str, database: str) -> Optional[Users]:
        return db.query(Users).filter(Users.guid == id, Users.scientometric_database == database).first()

    def get_multi_users(self, db: Session, filter: str, skip: int = 0, limit: int = 10) -> list[Type[Users]]:
        return db.query(Users).filter(Users.scientometric_database == filter).offset(skip).limit(limit).all()

    def get_stat_groupby_scientometric(self, db: Session) -> list[Row[StatGet]]:
        return db.query(Users.scientometric_database, func.sum(Users.document_count).label('documents_sum'),
                        func.sum(Users.citation_count).label('citations_sum'),
                        func.avg(Users.h_index).label('average_h_index')).group_by(Users.scientometric_database).all()


user = CRUDUser(Users)
