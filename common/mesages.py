PORT = 5522
"""Connection port for client-server connection."""

COMMAND_NAME_SEPARATOR = ":"
"""Separates command name from command arguments"""

COMMAND_ARG_SEPARATOR = "|"
"""Separates command arguments"""

CMD_DISCONNECT = ""
"""Sends a disconnect request to receiver. This terminates the connection."""

CMD_GET_CHAMPIONS = "GET_CHAMPS"
"""Requests a CSV formatted list of champions."""