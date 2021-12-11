import sys
from datetime import datetime, timezone

from sqlalchemy import (
    Column, VARCHAR, BOOLEAN, TIMESTAMP, func, DECIMAL, ForeignKey, UniqueConstraint, INTEGER,
    select, Index, text, NUMERIC,
)
from sqlalchemy.dialects.postgresql import ENUM, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref


Base = declarative_base()
quantity_decimal = DECIMAL(30, 18)


class Id(object):
    id = Column(INTEGER, primary_key=True)


class CreatedTracked(object):
    created_at = Column(TIMESTAMP(True), nullable=False, server_default=func.now())
    created_by = Column(VARCHAR, nullable=False, default=sys.argv[0])


class Tracked(CreatedTracked):
    updated_at = Column(TIMESTAMP(True), nullable=False, server_default=func.now(), onupdate=lambda: datetime.now(timezone.utc))
    updated_by = Column(VARCHAR, nullable=False, default=sys.argv[0])


class User(Base, Id):
    __tablename__ = 'user'
    username = Column(VARCHAR, nullable=False)
