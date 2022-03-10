from collections import Callable
import common
import socket

onMessage: Callable[[socket.socket, str, list[str]], None] = None
_connection: socket.socket = None


def disconnect() -> None:
    """Disconnect from the server. If server is not connected, this has no effect."""
    global _connection
    if _connection is None:
        return
    
    _connection.close()
    _connection = None


def connect() -> None:
    """Connects to the server. If server is connected, the previous connection is disconnected."""
    global _connection
    if _connection is not None:
        disconnect()

    HOST = "localhost"
    _connection =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _connection.connect((HOST, common.PORT))


def sendMessage(message: str, args: list[str]) -> str:
    """Sends a request to the server. Returns the response."""
    global _connection
    if message == common.MSG_DISCONNECT:
        disconnect()
        return
    if _connection is None:
        connect()

    request = f"{message}:{'|'.join(args)}"
    _connection.send(request.encode("utf8"))
    response = _connection.recv(common.MSG_SIZE).decode("utf8")
    return response
