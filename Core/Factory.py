import _pickle
import os
import pickle
from abc import ABC
from pathlib import Path

from twisted.internet.protocol import connectionDone
from twisted.protocols.basic import NetstringReceiver

from twisted.internet import protocol

from Cryptography.crypto_data import (
    encrypt_data_by_key_with_fernet,
    decrypt_data_by_key_with_fernet,
)

from Utils.string_utils import generate_random_string


__ALL_PROTOCOLS__ = {}

from twisted.python import failure


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
        self.factory.clients['no_inited'].append(self)

    def stringReceived(self, data):
        self._buffer += data

        self.compare_message(data)

    def connectionLost(self, reason=connectionDone):
        if self in self.factory.clients['no_inited']:
            self.factory.clients['no_inited'].remove(self)
        if self.encryption.key in self.factory.clients['inited']:
            self.factory.clients['inited'].pop(self.encryption.key)

    def convert_message(self, message):
        data = pickle.dumps(message)
        response = self.encryption.rsa_encrypt(data)
        return response


class FlatProtocol(NetstringReceiver, ABC):
    """ Обработчик соездиенния между сервером и клиентом. """
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
        # self._buffer += data
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
        self.name = 'SSLFactory'
        self.key_name = 'controller'


class MainProtocol(NetstringReceiver, ABC):

    def connectionMade(self):
        pass

    def stringReceived(self, data):
        cipher = pickle.loads(data)


class MainServer(protocol.Factory):
    protocol = MainProtocol

    def __init__(self, root):
        self.root = root


class ServerInitializerProtocol(NetstringReceiver, ABC):
    key: bytes
    invite_code: bytes
    invite_code: str

    def update_key(self):
        with open(f'{PARENT_PATH}/server_data/server.key', 'wb') as f:
            f.write(self.key)

    @staticmethod
    def key_path_exists():
        return os.path.exists(f'{PARENT_PATH}/server_data/server.key')

    @staticmethod
    def get_key():
        if os.path.exists(f'{PARENT_PATH}/server_data/server.key'):
            with open(f'{PARENT_PATH}/server_data/server.key', 'rb') as f:
                return f.read()
        else:
            return b""

    @staticmethod
    def get_saved_ip():
        if os.path.exists(f'{PARENT_PATH}/server_data/server_ip'):
            with open(f'{PARENT_PATH}/server_data/server_ip', 'rb') as f:
                return f.read()
        else:
            return b""

    def save_new_ip(self):
        with open(f'{PARENT_PATH}/server_data/server_ip', 'wb') as f:
            f.write(self.transport.getHost().host.encode())

    def save_invite_code(self):
        with open(f'{PARENT_PATH}/server_data/invite_code', 'w') as f:
            f.write(self.invite_code)

    @staticmethod
    def get_invite_code():
        if os.path.exists(f'{PARENT_PATH}/server_data/invite_code'):
            with open(f'{PARENT_PATH}/server_data/invite_code', 'r') as f:
                return f.read()
        else:
            return ""

    def connectionMade(self):
        key = self.get_key()
        host = self.transport.getHost().host
        invite_code = self.get_invite_code()

        if not invite_code:
            self.invite_code = generate_random_string(25)
            self.save_invite_code()

        if key:
            pair = encrypt_data_by_key_with_fernet(host, key)
        else:
            pair = encrypt_data_by_key_with_fernet(host)

        cipher = pair['cipher']

        self.key = pair['key']

        if not self.key_path_exists():
            self.update_key()
            self.save_new_ip()

        else:
            if self.get_saved_ip() != host:
                self.save_new_ip()

        data = {'cipher': cipher, 'invite_code': invite_code}
        self.sendString(pickle.dumps(data))


class ServerInitializerFactory(protocol.ReconnectingClientFactory):
    protocol = ServerInitializerProtocol
