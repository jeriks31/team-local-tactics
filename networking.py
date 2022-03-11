from core import Champion
from json import dumps, loads
from socket import socket, AF_INET, SOCK_STREAM

PORT = 5522
"""Server will be listening on this port."""

MSG_MATCH_STARTED = "MATCH_STARTED"
"""Server -> Client: The match has started."""

MSG_MATCH_ENDED = "MATCH_ENDED"
"""Server -> Client: The match has ended. """

MSG_PICK_CHAMPION = "PICK_CHAMPION"
"""Server -> Client: Pick a champion."""

MSG_PICKED_CHAMPION = "PICKED_CHAMPION"
"""Client -> Server: A champion is picked."""

def send_message(connection:socket, message:str,args:list[str]) -> None:
    """Sends a messages through the connection."""
    request = f"{message}:{'|'.join(args)}"
    connection.send(request.encode("utf8"))

def receive_message(connection:socket) -> (str, list[str]):
    """Receives a message through the connection. Returns (message_name, message_arguments)."""
    response = connection.recv(2048).decode("utf8").split(':')
    message = response[0]
    args = response[1].split('|') if len(response) > 1 else []
    return (message, args)

def new_connection() -> socket:
    return socket(AF_INET, SOCK_STREAM)