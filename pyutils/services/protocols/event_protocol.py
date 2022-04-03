from pyutils.services.enums.enum_type import BaseEnum
from pyutils.services.enums.protocol_enum import MessageTypes
from pyutils.services.protocols.message_protocol import MessageProtocol


class EventProtocol(MessageProtocol):
    callbacks = {}

    def __init__(self, *args, **kwargs):
        super(EventProtocol, self).__init__(*args, **kwargs)
        self.register_events()

    def register_events(self):
        ...

    def dataReceived(self, data: bytes):
        data = super(EventProtocol, self).dataReceived(data)

        if type(data) == dict:
            if data['key'] == MessageTypes.Event:
                if data["event"] in self.callbacks:
                    self.callbacks[data["event"]]()

    @classmethod
    def on(cls, event: BaseEnum, callback: callable):
        cls.callbacks[event] = callback
