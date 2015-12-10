/solaron/gateway
---

The GatewayServer is a websocket server that processes all real-time requests from the game client. ex. login, match making, etc

- All messages are transmitted with protocol buffers.
- Server is built on Autobaun[Twisted]
- Client is a simple websocket client used for testing, not meant for production.

/solaron/tests
---

test_gateway.py is a set of integration tests for interacting with a running GatewayServer

/bin
---
various tools

- generate_gateway_messages.py




Dependencies
---

Autobaun (http://autobahn.ws/python/installation.html)
Protocol Buffers (https://developers.google.com/protocol-buffers/)


