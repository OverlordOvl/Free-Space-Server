from Crypto.verification import init_verification
from Factory import SSLFactory, FlatFactory
from twisted.internet import reactor


class Controller:

    def __init__(self):
        # self.model = model.ClientModel(self)
        self.reactor = reactor
        # self.api = API(self)

    def run_server(self):
        self.add_channel(
            FlatFactory(self), 41387
        )
        # self.add_channel(
        #     SSLFactory(self), 41387
        #     )
        print("Server run")
        self.reactor.run()

    def stop_server(self):
        self.reactor.stop()

    def add_channel(self, factory, port):
        self.reactor.listenTCP(port, factory)
    #     self.reactor.listenSSL(port, factory, init_verification(factory))


Controller().run_server()
