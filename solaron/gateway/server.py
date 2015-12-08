"""gateway_server

Usage:
    gateway_server.py [options]

Options:
    -p --port PORT   Port to listen on [default: 9000].
    -d --debug       Debug enabled? [default: False]
"""

import sys

from docopt import docopt

from autobahn.twisted.choosereactor import install_optimal_reactor
install_optimal_reactor()

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

from _message_factory import GatewayMessageFactory

class GatewayServerProtocolError(Exception):
    pass

class GatewayServerProtocolFactory(WebSocketServerFactory):
    def __init__(self, *args, **kargs):
        WebSocketServerFactory.__init__(self, *args, **kargs)

        self.protocol = GatewayServerProtocol
        self.messageFactory = GatewayMessageFactory()

class GatewayServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {} ({})".format(request.peer, self))

    def onOpen(self):
        print("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            #figure out how to configure protocol to catch this at a higher level?
            raise GatewayServerProtocolError("Only binary messages supported")

        message = self.factory.messageFactory.decodeMessage(payload)

        self._processMessage(message)

    def _processMessage(self, message):
        print("message = {}".format(message))


if __name__ == '__main__':

    args = docopt(__doc__)

    log.startLogging(sys.stdout)

    reactor.listenTCP(
        int(args['--port']), 
        GatewayServerProtocolFactory(debug=args['--debug']))
    reactor.run()

