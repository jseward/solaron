import unittest

#for these imports to work setup the PYTHONPATH environment variable to contain solaron root (ex. c:\dev\solaron\solaron)
from gateway.client import GatewayClient
from gateway._messages_pb2 import LoginRequestMessage, SUCCESS

GATEWAY_ADDRESS = "localhost"
GATEWAY_PORT = 9000
CLIENT_TIMEOUT = 5

class Client:

    def __init__(self, account):
        self.account = account
        self.innerClient = GatewayClient(GATEWAY_ADDRESS, GATEWAY_PORT, CLIENT_TIMEOUT)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.innerClient.disconnect()

    def connect(self):
        self.innerClient.connect()

    def loginWithSteamId(self, shouldVerifyResponse=True):
        return self._checkResponse(self.innerClient.loginWithSteamId(self.account.steamId), shouldVerifyResponse)

    def _checkResponse(self, response, shouldVerifyResponse):
        if shouldVerifyResponse:
            if response.statusCode != OK:
                raise ClientError("StatusCode expected to be OK but instead is {} : {}".format(response.statusCode, response))
        return response

class Account:
    def __init__(self, steamId):
        self.steamId = steamId

class GatewayTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def createAccount(self):
        steamId = 123 #todo - generate random steamId
        return Account(steamId)

    def createClient(self):
        return Client(self.createAccount())

class LoginTestCase(GatewayTestCase):
    def testLoginWillSucceed(self):
        with self.createClient() as client:
            client.connect()
            response = client.loginWithSteamId(shouldVerifyResponse=False)
            self.assertEqual(response.status_code, SUCCESS)


if __name__ == "__main__":
    unittest.main()
