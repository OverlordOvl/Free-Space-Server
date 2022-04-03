from twisted.internet.protocol import Protocol

from pyutils.services.protocols.context_protocol import ContextProtocol
from pyutils.services.protocols.event_protocol import EventProtocol
from pyutils.services.protocols.message_protocol import MessageProtocol
from pyutils.services.protocols.user_protocol import UserProtocol


class MainProtocol(
    UserProtocol, EventProtocol
):

    def __init__(self):
        super(MainProtocol, self).__init__()
