"""gateway_client

Usage:
    gateway_client.py [options]

Options:
    -a --address ADDRESS    Address to connect to [default: localhost]
    -p --port PORT          Port to connect to [default: 9000].
"""

import base64

if __name__ == '__main__':

    from docopt import docopt
    args = docopt(__doc__)

    from websocket import create_connection
    url = "ws://" + args['--address'] + ":" + args['--port']
    ws = create_connection(url)
    print "Sending 'Hello, World'..."
    ws.send_binary(base64.b64encode(b"Hello, World"))
    print "Sent"
    print "Receiving..."
    result = ws.recv()
    print "Received '%s'" % result
    ws.close()





