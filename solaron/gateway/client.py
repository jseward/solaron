"""gateway_client

Usage:
    gateway_client.py [options]

Options:
    -a --address ADDRESS    Address to connect to [default: localhost]
    -p --port PORT          Port to connect to [default: 9000]
    -d --debug              Debug enabled? [default: False]
    --steam_id              steam_id to login with [default: 1]
"""

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol

from _message_factory import GatewayMessageFactory
from _messages_pb2 import LoginRequestMessage

class GatewayClientError(Exception):
    pass

class GatewayClient:
    def runWithSteamIdLogin(self, address, port, steam_id, debug):
        open_message = LoginRequestMessage()
        open_message.steam_id = steam_id

        reactor.connectTCP(
            address,
            port, 
            GatewayClientProtocolFactory(open_message, debug=debug))
        reactor.run()

class GatewayClientProtocolFactory(WebSocketClientFactory):
    def __init__(self, open_message, *args, **kargs):
        WebSocketClientFactory.__init__(self, *args, **kargs)

        self.protocol = GatewayClientProtocol
        self.messageFactory = GatewayMessageFactory()
        self.openMessage = open_message

class GatewayClientProtocol(WebSocketClientProtocol):

    def onConnect(self, request):
        print("Server Connected: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        if self.factory.openMessage:
            print("sending open message : {}".format(self.factory.openMessage))
            self.sendMessage(self.factory.messageFactory.encodeMessage(self.factory.openMessage), isBinary=True)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            #figure out how to configure protocol to catch this at a higher level?
            raise GatewayClientError("Only binary messages supported")

        message = self.factory.messageFactory.decodeMessage(payload)

        _processMessage(message)

    def _processMessage(message):
        print("message = {}".format(message))


if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)

    client = GatewayClient()
    client.runWithSteamIdLogin(
        args['--address'], 
        int(args['--port']), 
        int(args['--steam_id']), 
        args['--debug'])
