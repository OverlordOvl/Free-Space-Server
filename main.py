from Core import settings
from Core.Factory import FlatFactory, ServerInitializerFactory, MainServer
from twisted.internet import reactor


main_server_ip = 'localhost'


class Controller:

    def __init__(self):
        self.reactor = reactor

    def run_server(self):
        self.add_channel(
            FlatFactory(self), 41387
        )
        self.add_channel(
            MainServer(self), 8000
        )
        self.connect_to_main_server(
            main_server_ip, 8000,
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
    #     self.reactor.listenSSL(port, factory, init_verification(factory))


Controller().run_server()