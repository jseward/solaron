"""gateway_server

Usage:
    gateway_server.py [options]

Options:
    -p --port PORT   Port to listen on [default: 9000].
"""

if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)

    from autobahn.twisted.choosereactor import install_optimal_reactor
    install_optimal_reactor()

    import sys
    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout)

    from gateway_server_protocol import GatewayServerProtocol
    from autobahn.twisted.websocket import WebSocketServerFactory
    factory = WebSocketServerFactory()
    factory.protocol = GatewayServerProtocol

    port = int(args['--port'])

    reactor.listenTCP(port, factory)
    reactor.run()

