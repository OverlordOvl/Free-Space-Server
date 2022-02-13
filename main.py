import os

from pyutils.server.controller import FlatFactory, ServerInitializerFactory
from twisted.internet import reactor
from dotenv import load_dotenv


load_dotenv()

MAIN_SERVER_IP = '5.142.251.207'


class Controller:

    def __init__(self):
        self.reactor = reactor

    def run_server(self):
        self.add_channel(
            FlatFactory(self), 80
        )
        # self.add_channel(
        #     MainServer(self), int(os.getenv('PRIMARY_SERVER_PORT'))
        # )
        self.connect_to_main_server(
            MAIN_SERVER_IP, 8000,
            ServerInitializerFactory()
        )
        # self.add_channel(
        #     SSLFactory(self), 41387
        #     )
        print("Server run")
        self.reactor.run()

    def connect_to_main_server(self, server, port, factory):
        reactor.connectTCP(server, port, factory)

    def stop_server(self):
        self.reactor.stop()

    def add_channel(self, factory, port):
        self.reactor.listenTCP(port, factory)


Controller().run_server()
