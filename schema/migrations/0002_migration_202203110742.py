# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class AccessToken(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime(2022, 3, 11, 7, 42, 21, 625667))
    expires_at = DateTimeField()
    active = BooleanField(default=True)
    value = CharField(max_length=140, unique=True)
    class Meta:
        table_name = "accesstoken"


@snapshot.append
class RefreshToken(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    created_at = DateTimeField(default=datetime.datetime(2022, 3, 11, 7, 42, 21, 625667))
    expires_at = DateTimeField()
    active = BooleanField(default=True)
    value = CharField(max_length=140, unique=True)
    class Meta:
        table_name = "refreshtoken"


def forward(old_orm, new_orm):
    accesstoken = new_orm['accesstoken']
    refreshtoken = new_orm['refreshtoken']
    return [
        # Apply default value True to the field accesstoken.active,
        accesstoken.update({accesstoken.active: True}).where(accesstoken.active.is_null(True)),
        # Apply default value True to the field refreshtoken.active,
        refreshtoken.update({refreshtoken.active: True}).where(refreshtoken.active.is_null(True)),
    ]
