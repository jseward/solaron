from enum import Enum

import _messages

class GatewayServerMessageFactoryError(Exception):
    pass

class GatewayServerMessageId(Enum):
    LOGIN_REQUEST = 1
    LOGIN_RESPONSE = 2

class GatewayServerMessageFactory:
    
    def __init__(self):
        self._messageMap = {
            GatewayServerMessageId.LOGIN_REQUEST: _messages.LoginRequestMessage,
            GatewayServerMessageId.LOGIN_RESPONSE: _messages.LoginResponseMessage
        }

    def decodeMessage(self, data):
        if not isinstance(data, bytes):
            raise GatewayServerMessageFactoryError("decodeMessage expects data to be of type 'bytes'")

        if len(data) < 1:
            raise GatewayServerMessageFactoryError("decodeMessage requires at least one byte for header")

        from struct import unpack
        message_id = unpack("B", data[0])[0]
        
        return self._messageMap[GatewayServerMessageId(message_id)]()


if __name__ == '__main__':
    factory = GatewayServerMessageFactory()
    print (factory.decodeMessage(b"\x02"))
