import os
import pickle
from abc import ABC
from pathlib import Path

from loguru import logger
from twisted.internet.protocol import connectionDone
from twisted.protocols.basic import NetstringReceiver

from twisted.internet import protocol

from crypto.crypto_data import (
    decrypt_data_by_key_with_fernet, encrypt_data_by_key_with_fernet,
)

from pyutils.string_utils import generate_random_string

from twisted.python import failure
from dotenv import load_dotenv

from pyutils.server.server import get_server, register_server
from schema.models import Server


load_dotenv()

__ALL_PROTOCOLS__ = {}

FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PARENT_PATH = str(Path(FILE_PATH).parent)



class ClientsController:
    def __init__(self):
        self.clients = {}

    def connection_made(self, client):
        if client.id not in self.clients or not client.id:
            id_ = max(self.clients) + 1 if self.clients else 1
            client.id = id_
            client.alive = True
            self.clients[id_] = client
        else:
            id_ = client.id
            self.clients[id_] = client

    def connection_lost(self, client):
        self.clients[client.id].alive = False


class User:
    id: int = 0
    token: bytes
    alive: bool


class SSLProtocol(NetstringReceiver, ABC):
    def __init__(self):
        super(SSLProtocol, self).__init__()
        self.first_connection = True

    def connectionMade(self):
        self.factory.clients["no_inited"].append(self)

    def stringReceived(self, data):
        self._buffer += data

        self.compare_message(data)

    def connectionLost(self, reason=connectionDone):
        if self in self.factory.clients["no_inited"]:
            self.factory.clients["no_inited"].remove(self)
        if self.encryption.key in self.factory.clients["inited"]:
            self.factory.clients["inited"].pop(self.encryption.key)

    def convert_message(self, message):
        data = pickle.dumps(message)
        response = self.encryption.rsa_encrypt(data)
        return response


class FlatProtocol(NetstringReceiver, ABC):
    """Обработчик соездиенния между сервером и клиентом."""

    client: User

    def __init__(self):
        super(FlatProtocol, self).__init__()
        self.first_connection = True

    def connectionMade(self):
        if self.first_connection:
            self.client = User()
            self.client.protocol = self
            self.first_connection = False
        self.factory.controller.connection_made(self.client)

    def connectionLost(self, reason: failure.Failure = connectionDone):
        self.factory.controller.connection_lost(self.client)

    def stringReceived(self, data):
        self.compare_message(data)


class FlatFactory(protocol.Factory):
    protocol = FlatProtocol

    def __init__(self, root):
        self.root = root
        self.controller = ClientsController()


class SSLFactory(protocol.Factory):
    protocol = SSLProtocol

    def __init__(self, root):
        self.root = root
        self.name = "SSLFactory"
        self.key_name = "controller"


class MainProtocol(NetstringReceiver, ABC):

    # TODO Удалить данный класс. Является тестовым

    def connectionMade(self):
        pass

    def stringReceived(self, data):
        data = pickle.loads(data)
        ip = decrypt_data_by_key_with_fernet(data['cipher'], data['key'])


class MainServer(protocol.Factory):
    protocol = MainProtocol

    def __init__(self, root):
        self.root = root


class ServerInitializerProtocol(NetstringReceiver, ABC):
    key: str
    invite_code: str
    server: Server

    def connectionMade(self):
        host = self.transport.getHost().host
        server = get_server()

        if not server:
            cipher, self.key = encrypt_data_by_key_with_fernet(host)
            self.key = self.key.decode("utf-8")
            self.invite_code = generate_random_string(25)
            server = register_server(self.key, host, self.invite_code)
        else:
            self.invite_code = server.invite_code
            self.key = server.key
            cipher = encrypt_data_by_key_with_fernet(host, self.key)[0]

        self.server = server
        logger.success(f"Your invite code is {self.invite_code}")
        self.sendString(
            # TODO Удалить ключ key. Является тестовым
            pickle.dumps({"cipher": cipher, "invite_code": self.invite_code, "key": self.key})
        )


class ServerInitializerFactory(protocol.ReconnectingClientFactory):
    protocol = ServerInitializerProtocol
