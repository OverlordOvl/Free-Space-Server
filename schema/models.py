import os
import sys
import datetime
from dotenv import load_dotenv
from peewee import BooleanField, PostgresqlDatabase

from peewee import CharField, DateTimeField, PrimaryKeyField, Model, IPField, ForeignKeyField


load_dotenv()

db_handle = PostgresqlDatabase(
    database=os.getenv('PGDATABASE'),
    user=os.getenv('PGUSER'),
    password=os.getenv('PGPASSWORD'),
    host=os.getenv('PGHOST')
)


class DBModel(Model):
    class Meta:
        database = db_handle


class BaseModel(DBModel):
    id = PrimaryKeyField(null=False)


class CreatedTracked(DBModel):
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())


class Server(BaseModel):
    ip = IPField()
    key = CharField(max_length=44, unique=True)
    invite_code = CharField(max_length=255, unique=True)


class User(BaseModel):
    username = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)


class AuthToken(BaseModel):
    user = ForeignKeyField(User)
    token = CharField(max_length=100)
    validity_time = DateTimeField()
    is_active = BooleanField(default=False)
