from twisted.internet.protocol import Factory

from pyutils.db.daos.token import create_auth_token
from pyutils.services.protocols.api_protocol import ApiProtocol
from pyutils.services.protocols.user_protocol import UserProtocol


class AuthenticationAPI(ApiProtocol, UserProtocol):
    def register_events(self):
        super(AuthenticationAPI, self).register_events()
        self.on("create_auth_token", lambda: self.create_auth_token)

    def create_token(self):
        new_token = create_auth_token(self.user_id)
        # self.write()
