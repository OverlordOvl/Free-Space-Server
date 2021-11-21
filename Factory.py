import _pickle
import pickle
from abc import ABC

from twisted.internet.protocol import connectionDone
from twisted.protocols.basic import NetstringReceiver

from twisted.internet import protocol


__ALL_PROTOCOLS__ = {}


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
        pass


class User:
    id: int
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

    def compare_message(self, data):
        response = None
        message = None
        decryption = None
        try:
            if "exec" in str(data) or "eval" in str(data):
                pass
            else:
                try:
                    message = pickle.loads(data)
                    decryption = None
                except KeyError:
                    message = None
                    decryption = None
                except _pickle.UnpicklingError:
                    decryption = self.encryption.rsa_decrypt(data)
                except UnicodeDecodeError:
                    decryption = self.encryption.rsa_decrypt(data)
                except OverflowError:
                    decryption = self.encryption.rsa_decrypt(data)
                except ValueError:
                    decryption = self.encryption.rsa_decrypt(data)
                except TypeError:
                    i = 0

                if decryption and message is None:
                    message = pickle.loads(decryption)

                if message:
                    if type(message) is bytes and len(message) == 44:
                        if not self.encryption.new_key(message):
                            self.connectionLost()
                        if self in self.factory.clients['no_inited']:
                            self.factory.clients['no_inited'].remove(self)
                        if self.encryption.key.decode() not in \
                            self.factory.clients['inited']:
                            self.factory.clients['inited'].update(
                                {
                                    self.encryption.key.decode(): [
                                        {'factory': self, 'client': None}]}
                            )
                        else:
                            self.factory.clients['inited'][
                                self.encryption.key.decode()].append(
                                {'factory': self, 'client': None}
                            )
                        self.clearLineBuffer()

                    else:
                        self.clearLineBuffer()

                        if "exec" in str(message) or "eval" in str(message):
                            pass
                        else:

                            message = pickle.loads(
                                self.encryption.rsa_decrypt(data)
                            )
                            if message:
                                api_response = self.factory.root.api.method(
                                    message['method'], message['values'],
                                    message['session'], factory=self
                                )
                                result = pickle.dumps(api_response)
                                encrypted_mess = self.encryption.rsa_encrypt(
                                    result
                                )
                                package_len = len(str(encrypted_mess))

                                response = pickle.dumps(
                                    {
                                        'len':  package_len,
                                        'mess': encrypted_mess}
                                )
                                response = encrypted_mess
                                print("Размер пакета -", package_len)

                            if response:
                                self.sendLine(response)

        except _pickle.UnpicklingError:
            pass

    def convert_message(self, message):
        data = pickle.dumps(message)
        response = self.encryption.rsa_encrypt(data)
        return response


class FlatProtocol(NetstringReceiver, ABC):
    client: User

    def __init__(self):
        super(FlatProtocol, self).__init__()
        self.first_connection = True

    def connectionMade(self):
        if self.first_connection:
            self.client = User()
            self.client.protocol = self
            self.first_connection = False
        self.sendString(b"Hello world!")

    def stringReceived(self, data):
        # self._buffer += data
        self.compare_message(data)


class FlatFactory(protocol.Factory):
    protocol = FlatProtocol

    def __init__(self, root):
        self.root = root


class SSLFactory(protocol.Factory):
    protocol = SSLProtocol

    def __init__(self, root):
        self.root = root
        self.name = 'SSLFactory'
        self.key_name = 'controller'
