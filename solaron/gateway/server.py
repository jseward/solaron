"""gateway_server

Usage:
    gateway_server.py [options]

Options:
    -p --port PORT   Port to listen on [default: 9000].
"""

import sys

from docopt import docopt

from autobahn.twisted.choosereactor import install_optimal_reactor
install_optimal_reactor()

from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor

from _server_protocol import GatewayServerProtocolFactory, GatewayServerProtocol

if __name__ == '__main__':

    args = docopt(__doc__)

    log.startLogging(sys.stdout)

    reactor.listenTCP(
        int(args['--port']), 
        GatewayServerProtocolFactory())
    reactor.run()

