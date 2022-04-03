# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class AccessToken(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime(2022, 3, 11, 7, 6, 4, 818093))
    expires_at = DateTimeField()
    value = CharField(max_length=140, unique=True)
    class Meta:
        table_name = "accesstoken"


@snapshot.append
class RefreshToken(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime(2022, 3, 11, 7, 6, 4, 818093))
    expires_at = DateTimeField()
    value = CharField(max_length=140, unique=True)
    class Meta:
        table_name = "refreshtoken"


