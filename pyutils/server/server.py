from datetime import datetime, timedelta

from pyutils.string_utils import generate_token, md5_string
from schema.models import Server


def register_server( key: str, ip: str, invite_code: str):
    server = Server.select().where(Server.key == key, Server.ip == ip, Server.invite_code == invite_code)
    if not server.exists():
        return Server.create(key=key, ip=ip, invite_code=invite_code)
    else:
        return server.get()


def get_server():
    return Server.select().first()
