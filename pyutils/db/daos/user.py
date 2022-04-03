from pyutils.db.daos.token import create_auth_token, create_refresh_token
from pyutils.utils import generate_token
from schema.models import AccessToken, RefreshToken, User


def create_user(username: str) -> User | None:
    try:
        return User().create(
            username=username,
            personal_token=generate_token(2048),
        )
    except:
        raise


def create_user_and_auth_token(
    username: str,
) -> list[User, AccessToken, RefreshToken]:
    user = create_user(username)
    if user:
        auth_token = create_auth_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return [user, auth_token, refresh_token]
    else:
        pass
