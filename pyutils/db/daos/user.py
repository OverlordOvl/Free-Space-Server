from datetime import datetime, timedelta

from pyutils.string_utils import generate_token, md5_string
from schema.models import AuthToken, User


def get_all_users():
    return User.select().all()


def authenticate(username: str, password: str):
    user = User.filter_by(username=username, password=md5_string(password)).first()
    if user:
        token = AuthToken.filter_by(user=user.id).first()
        if not token:
            token_value = generate_token(4)
            validity_time = datetime.now() + timedelta(weeks=1)
            return AuthToken().create(user=user.id, token=token_value, validity_time=validity_time)
        return token
    return


def create_user(username: str, password: str):
    return User.create(username=username, password=md5_string(password))
