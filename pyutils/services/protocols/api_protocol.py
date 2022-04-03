import warnings
from pyutils.services.protocols.event_protocol import EventProtocol
from pyutils.utils import snake_to_camel


class ApiProtocol(EventProtocol):
    prefix: str = ""

    def __init_subclass__(cls, **kwargs):
        if "api" not in cls.__name__.lower():
            warnings.warn(
                f'The prefix "API" must be present in the name of the protocol\n'
                f"Hint: you have installed {cls.__name__} but there must be a named {snake_to_camel(cls.__name__ + '_API')}",
                SyntaxWarning,
            )
        cls.prefix = cls.__name__.lower().replace("api", "")

    @classmethod
    def on(cls, event: str, callback: callable):
        cls.callbacks[f"{cls.prefix}:{event}"] = callback
