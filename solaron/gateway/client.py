"""client

Usage:
    client.py [options]

Options:
    -a --address ADDRESS    Address to connect to [default: localhost]
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

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._disconnect()

    def _getUrl(self):
        return "ws://{}:{}".format(self.address, self.port)

    def _connect(self):
        self._connection = create_connection(self._getUrl(), timeout=self.timeout)

    def _disconnect(self):
        self._connection.close()

    def loginWithSteamId(self, steam_id):
        if not self._connection.connected:
            raise GatewayClientError("not connected")

        request = LoginRequestMessage()
        request.steam_id = steam_id
        return self._sendRequest(request, LoginResponseMessage)

    def _sendRequest(self, request, expected_response_class):
        request_data = self._messageFactory.encodeMessage(request)
        self._connection.send_binary(request_data)
        response_data = self._connection.recv()
        response = self._messageFactory.decodeMessage(response_data)        
        if not isinstance(response, expected_response_class):
            raise GatewayClientError("response received expected to be of type {} but is of type {}".format(expected_response_class, response.__class__))
        return response

if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)

    with GatewayClient(args['--address'], int(args['--port']), 5) as client:
        response = client.loginWithSteamId(int(args['--steam_id']))
        assert response.result == SUCCESS
