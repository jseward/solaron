import base64

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

from _message_factory import GatewayServerMessageFactory

#http://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python
class GatewayServerProtocolError(Exception):
    pass

class GatewayServerProtocolFactory(WebSocketServerFactory):
    def __init__(self):
        WebSocketServerFactory.__init__(self)

        self.protocol = GatewayServerProtocol
        self.messageFactory = GatewayServerMessageFactory()

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

        print (message)


