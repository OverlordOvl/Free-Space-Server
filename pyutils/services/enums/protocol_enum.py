from pyutils.services.enums.enum_type import BaseEnum


class MessageTypes(BaseEnum):
    Message = 'message'
    Event = 'event'


class ClientEvents(BaseEnum):
    Connection = 'connection'
    Authentication = 'authentication'
    AuthenticationRequest = 'authenticationRequest'
