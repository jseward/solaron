from enum import Enum

from _messages_pb2 import *

class GatewayMessageFactoryError(Exception):
    pass

class GatewayMessageFactory:
    
    def __init__(self):
        self._messageMap = {
            LOGIN_REQUEST: LoginRequestMessage,
            LOGIN_RESPONSE: LoginResponseMessage
        }

    def encodeMessage(self, message):
        message_id = self._getMessageIdOfMessage(message)

        from struct import pack
        data_header = pack("B", message_id)

        data = message.SerializeToString()

        return data_header + data        

    def decodeMessage(self, data):
        if not isinstance(data, bytes):
            raise GatewayMessageFactoryError("decodeMessage expects data to be of type 'bytes'")

        if len(data) < 1:
            raise GatewayMessageFactoryError("decodeMessage requires at least one byte for header")

        from struct import unpack
        message_id = unpack("B", data[0])[0]
        
        if not self._messageMap.has_key(message_id):
            raise GatewayMessageFactoryError("decodeMessage found unexpected message_id in header : {}".format(message_id))

        message = self._messageMap[message_id]()
        message.ParseFromString(data[1:])
        return message_id, message

    def _getMessageIdOfMessage(self, message):
        for k, v in self._messageMap.items():
            if isinstance(message, v):
                return k
        
        raise GatewayMessageFactoryError("no message_id exists for message : {}".format(message))


if __name__ == '__main__':
    factory = GatewayMessageFactory()

    test_message = LoginRequestMessage()
    test_message.steam_id = 123

    data = factory.encodeMessage(test_message)
    decoded_message = factory.decodeMessage(data)

    assert test_message == decoded_message



