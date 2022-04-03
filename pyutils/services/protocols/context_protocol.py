from typing_extensions import Protocol


class ContextProtocol(Protocol):
    context: dict = {}

    def set_context(self, key, value):
        self.context[key] = value

    def get_context(self, key):
        return self.context.get(key)
