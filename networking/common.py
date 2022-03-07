PORT = 5522
"""Server will be listening on this port."""
MSG_SIZE = 2048
"""Size of message buffer."""

MSG_ARG_SEP = "|"
"""Separates message arguments."""

MSG_CMD_SEP = ":"
"""Separates message from arguments."""

MSG_DISCONNECT = "DISCONNECT"
"""From client to server: Signals a wish to disconnect. Connection will be closed. Disconnect messages should NOT expect a response."""

MSG_CONNECT = "CONNECT"
"""From client to server: Signals a client has connected."""