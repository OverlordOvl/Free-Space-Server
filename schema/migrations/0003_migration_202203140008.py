# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class User(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    username = CharField(max_length=50, unique=True)
    personal_token = CharField(max_length=2048, unique=True)
    class Meta:
        table_name = "user"


@snapshot.append
class AccessToken(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime(2022, 3, 14, 0, 8, 49, 200352))
    expires_at = DateTimeField()
    active = BooleanField(default=True)
    user = snapshot.ForeignKeyField(index=True, model='user')
    value = CharField(max_length=140, unique=True)
    class Meta:
        table_name = "accesstoken"


@snapshot.append
class RefreshToken(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime(2022, 3, 14, 0, 8, 49, 200352))
    expires_at = DateTimeField()
    active = BooleanField(default=True)
    user = snapshot.ForeignKeyField(index=True, model='user')
    value = CharField(max_length=140, unique=True)
    class Meta:
        table_name = "refreshtoken"


def forward(old_orm, new_orm):
    accesstoken = new_orm['accesstoken']
    refreshtoken = new_orm['refreshtoken']
    return [
        # Check the field `accesstoken.user` does not contain null values,
        # Check the field `refreshtoken.user` does not contain null values,
    ]
