# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class User(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    username = CharField(max_length=100)
    password = CharField(max_length=100)
    class Meta:
        table_name = "user"


@snapshot.append
class AuthToken(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    user = snapshot.ForeignKeyField(index=True, model='user')
    token = CharField(max_length=100)
    validity_time = DateTimeField()
    is_active = BooleanField(default=False)
    class Meta:
        table_name = "authtoken"


@snapshot.append
class Server(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    ip = IPField()
    key = CharField(max_length=255)
    invite_code = CharField(max_length=255)
    class Meta:
        table_name = "server"


