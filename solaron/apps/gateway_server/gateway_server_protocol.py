from autobahn.twisted.websocket import WebSocketServerProtocol

class GatewayServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {} ({})".format(request.peer, self))

    def onOpen(self):
        print("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def onMessage(self, payload, isBinary):
        ## echo back message verbatim
        self.sendMessage(payload, isBinary)

