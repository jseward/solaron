"""client

Usage:
    client.py [options]

Options:
    -a --address ADDRESS    Address to connect [default: localhost]
    -p --port PORT          Port to connect to [default: 9000]
    -d --debug              Debug enabled? [default: False]
    --steam_id              steam_id to login with [default: 1]
"""

from websocket import create_connection

from _message_factory import GatewayMessageFactory
from _messages_pb2 import *

class GatewayClientError(Exception):
    pass

class GatewayClient:

    def __init__(self, address, port, timeout=None):
        self.address = address
        self.port = port
        self.timeout = timeout
        self._messageFactory = GatewayMessageFactory()
        self._connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def _getUrl(self):
        return "ws://{}:{}".format(self.address, self.port)

    def isConnected(self):
        return self._connection != None and self._connection.connected

    def connect(self):
        if self.isConnected():
            raise GatewayClientError("already connected")
        
        try:
            self._connection = create_connection(self._getUrl(), timeout=self.timeout)
        except Exception as e:
            raise GatewayClientError("Connect to '{}' failed: {}".format(self._getUrl(), e))

    def disconnect(self):
        if self.isConnected():
            self._connection.close()

    def loginWithSteamId(self, steamId):
        if not self._connection.connected:
            raise GatewayClientError("not connected")

        request = LoginRequestMessage()
        request.handlingType = LoginRequestMessage.WITH_STEAM_ID
        request.steamId = steamId
        return self._sendRequest(request, LoginResponseMessage)

    def _sendRequest(self, request, expectedResponseClass):
        requestData = self._messageFactory.encodeMessage(request)
        self._connection.send_binary(requestData)
        responseData = self._connection.recv()
        responseMessageId, responseMessage = self._messageFactory.decodeMessage(responseData)        
        if not isinstance(responseMessage, expectedResponseClass):
            raise GatewayClientError("response received expected to be of type {} but is of type {}".format(expectedResponseClass, response.__class__))
        return responseMessage

if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)

    address = args['--address']
    port = int(args['--port'])
    timeout = 5
    steamId = int(args['--steam_id'])

    with GatewayClient(address, port, timeout) as client:
        response = client.loginWithSteamId(steamId)
        assert response.result == SUCCESS
