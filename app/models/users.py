# Sereda Semen
# 2022, 06.10
import enum
import time
from uuid import uuid4

from sqlalchemy import Column, Integer, String, func, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class scientometric_status(enum.Enum):
    scopus = 1
    wos = 2
    risc = 3


class Users(Base):
    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4,
                server_default=func.gen_random_uuid())
    full_name = Column(String(64), unique=True, nullable=False)
    scientometric_database = Column(Enum(scientometric_status))
    document_count = Column(Integer(), default=0, server_default='0')
    citation_count = Column(Integer(), default=0, server_default='0')
    h_index = Column(Integer(), default=0, server_default='0')
    url = Column(String)
    created_at = Column(Integer, default=int(time.time()),
                        server_default=func.extract('epoch', func.now()))
