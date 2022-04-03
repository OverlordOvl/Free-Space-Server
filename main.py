from twisted.internet import reactor

from pyutils.services.space_protocol import Space
from loguru import logger


main_server_ip = "localhost"


class Controller:

    def __init__(self):
        self.reactor = reactor

    def run_server(self):
        self.add_channel(Space(), 8000)
        logger.success("Server run")
        self.reactor.run()

    # def connect_to_main_server(self, server, port, factory):
    #     reactor.connectTCP(server, port, factory)

    def stop_server(self):
        self.reactor.stop()

    def add_channel(self, factory, port):
        logger.info(f"Add chanel on port: {port}. Provide by {factory.__class__.__name__} factory")
        self.reactor.listenTCP(port, factory)

    #     self.reactor.listenSSL(port, factory, init_verification(factory))


Controller().run_server()
