import datetime

import motor.motor_asyncio
from fastapi import Request
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import (
    as_declarative
)
from sqlalchemy.orm import sessionmaker, declared_attr
from elasticsearch import Elasticsearch
from pydantic import Field, BaseModel
from bson import ObjectId
from conf.settings.prod import settings
from core import exceptions as ex


# -------------
# ElasticSearch
# -------------
es = Elasticsearch(f'{settings.ELASTICSEARCH_URL}:{settings.ELASTICSEARCH_PORT}')
es.info()

# -------
# MONGODB
# -------
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
mongo = client.API


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseMongo(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MongoRequest(BaseMongo):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class MongoResponse(BaseMongo):
    id: PyObjectId


# -------
# Mariadb
# -------
if not settings.TEST_MODE:
    default_engine = create_engine(
        settings.POSTGRESQL_URL,
    )
else:
    default_engine = create_engine(
        settings.TEST_DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False}
    )

log_engine = create_engine(
    settings.LOGS_SQLITE_URL,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
)

DefaultSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=default_engine
)
LogSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=log_engine
)


def get_db(request: Request):
    return request.state.db


class Base:
    id: int = Column(Integer, primary_key=True, index=True)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """
        테이블명 지정
        Camel >> Snake
        """
        import re
        camel = re.compile(r'(.)([A-Z][a-z]+)')
        to_snake = re.compile('([a-z0-9])([A-Z])')
        return to_snake.sub(r'\1_\2', camel.sub(r'\1_\2', cls.__name__)).lower()

    @classmethod
    def get_object_or_404(cls, db, obj_id: int):
        obj = db.query(cls).filter(cls.id == obj_id).first()
        if obj is None:
            raise ex.DatabaseExceptions.NotFoundObject
        return obj


@as_declarative()
class DefaultBase(Base):
    pass


@as_declarative()
class LogBase(Base):
    pass


class TimeStamp:
    created = Column(
        DateTime,
        default=datetime.datetime.utcnow()
    )
    updated = Column(
        DateTime,
        default=datetime.datetime.utcnow(),
        onupdate=datetime.datetime.utcnow()
    )
