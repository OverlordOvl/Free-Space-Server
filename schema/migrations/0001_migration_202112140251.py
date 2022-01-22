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


