import os
import sys
import datetime
from dotenv import load_dotenv
from peewee import BooleanField, PostgresqlDatabase

from peewee import (
    CharField,
    DateTimeField,
    PrimaryKeyField,
    Model,
    IPField,
    ForeignKeyField,
)


load_dotenv()

db_handle = PostgresqlDatabase(
    database=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
)


class DBModel(Model):
    class Meta:
        database = db_handle


class BaseModel(DBModel):
    id = PrimaryKeyField(null=False)


class CreatedTracked(DBModel):
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())


class Expired(DBModel):
    created_at = DateTimeField(default=datetime.datetime.now())
    expires_at = DateTimeField()
    active = BooleanField(default=True)


class User(BaseModel):
    username = CharField(max_length=50, unique=True)
    personal_token = CharField(max_length=2048, unique=True)


class AccessToken(BaseModel, Expired):
    user = ForeignKeyField(User)
    value = CharField(max_length=140, unique=True)


class RefreshToken(BaseModel, Expired):
    user = ForeignKeyField(User)
    value = CharField(max_length=140, unique=True)
