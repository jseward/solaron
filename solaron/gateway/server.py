"""server

Usage:
    server.py [options]

Options:
    -p --port PORT   Port to listen on [default: 9000]
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
from _messages_pb2 import LOGIN_REQUEST
from _messages_pb2 import LoginRequestMessage, LoginResponseMessage
from _messages_pb2 import SUCCESS, ALREADY_LOGGED_IN

class GatewayServerError(Exception):
    pass

class GatewayServerProtocolFactory(WebSocketServerFactory):
    def __init__(self, *args, **kargs):
        WebSocketServerFactory.__init__(self, *args, **kargs)

        self.protocol = GatewayServerProtocol
        self.messageFactory = GatewayMessageFactory()
        
        self._nextClientId = 0
        self._loggedInClientMap = {}
        self._messageHandlerMap = {
            LOGIN_REQUEST: self._handleLoginRequest
        }

    def incrementClientId(self):
        prev = self._nextClientId
        self._nextClientId += 1
        return prev

    def handleMessage(self, protocol, messageId, message):
        if not self._messageHandlerMap.has_key(messageId):
            raise GatewayServerError("No message handler exists for messageId:{} ({})".format(messageId, message))
        self._messageHandlerMap[messageId](protocol, message)

    def _handleLoginRequest(self, protocol, message):
        print("Received LoginRequest : {}".format(protocol.peer))
        
        if self._loggedInClientMap.has_key(protocol.clientId):
            print("Client has already logged in! ClientId={} , Peer={}".format(protocol.clientId, protocol.peer))
            protocol.sendLoginResponseWithStatusCode(ALREADY_LOGGED_IN)
        else:
            if message.handlingType == LoginRequestMessage.WITH_STEAM_ID:
                self._handleLoginRequestWithSteamId(protocol, message)
            else:
                print("LoginRequest has unexpected handlingType : {}".format(message.handlingType))
                protocol.sendLoginResponseWithStatusCode(INVALID_LOGIN_REQUEST)

    def _handleLoginRequestWithSteamId(self, protocol, message):
        #TODO
        self._loggedInClientMap[protocol.clientId] = protocol
        response = LoginResponseMessage()
        response.statusCode = SUCCESS
        protocol.encodeAndSendMessage(response)

class GatewayServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        pass

    def onOpen(self):
        self.clientId = self.factory.incrementClientId()
        print("Client connected. peer={} , clientId={}".format(self.peer, self.clientId))

    def onClose(self, wasClean, code, reason):
        print("Client connection closed. clientId={} , reason={}".format(self.clientId, reason))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            #figure out how to configure protocol to catch this at a higher level?
            raise GatewayServerError("Only binary messages supported")

        messageId, message = self.factory.messageFactory.decodeMessage(payload)
        self.factory.handleMessage(self, messageId, message)

    def encodeAndSendMessage(self, message):
        self.sendMessage(self.factory.messageFactory.encodeMessage(message), isBinary=True)

    def sendLoginResponseWithStatusCode(self, statusCode):
        message = LoginResponseMessage()
        message.statusCode = statusCode
        self.encodeAndSendMessage(message)

if __name__ == '__main__':

    args = docopt(__doc__)

    log.startLogging(sys.stdout)

    reactor.listenTCP(
        int(args['--port']), 
        GatewayServerProtocolFactory(debug=args['--debug']))
    reactor.run()

