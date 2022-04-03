from pyutils.services.enums.protocol_enum import ClientEvents, MessageTypes
from pyutils.services.protocols.context_protocol import ContextProtocol
from pyutils.services.protocols.event_protocol import EventProtocol


class UserProtocol(EventProtocol, ContextProtocol):
    user_id: int
    token: str

    def __init__(self):
        super(UserProtocol, self).__init__()

    def register_events(self):
        self.on(ClientEvents.Connection, self.auth_user)

    def auth_user(self):
        self.send_message(MessageTypes.Event, event=ClientEvents.AuthenticationRequest)
