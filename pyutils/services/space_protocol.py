from loguru import logger
from twisted.internet.protocol import connectionDone, Factory
from twisted.python import failure

from pyutils.services.enums.protocol_enum import ClientEvents
from pyutils.services.protocols.main_protocol import MainProtocol


class SpaceProtocol(MainProtocol):

    def __init__(self):
        super(SpaceProtocol, self).__init__()

    def connectionMade(self):
        logger.success(f'New connection from {self.transport.getPeer().host}')

    def connectionLost(self, reason: failure.Failure = connectionDone):
        logger.info(f'Connection lost from {self.transport.getPeer().host}')

    def on_new_message(self, data):
        print(data)


class Space(Factory):
    protocol = SpaceProtocol
