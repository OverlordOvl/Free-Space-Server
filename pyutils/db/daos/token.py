import datetime

from pyutils.utils import generate_token
from schema.models import AccessToken, RefreshToken


def create_auth_token(user_id: int):
    return AccessToken.create(
        user=user_id,
        value=generate_token(140),
        expires_at=datetime.datetime.now() + datetime.timedelta(days=2),
    )


def create_refresh_token(user_id: int):
    return RefreshToken().create(
        user=user_id,
        value=generate_token(140),
        expires_at=datetime.datetime.now() + datetime.timedelta(weeks=2),
    )
