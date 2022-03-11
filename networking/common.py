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

def parse_champion(championText: str) -> Champion:
    name, rock, paper, scissors = championText.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))

def json_parse_champions(championTexts: str) -> dict[str, Champion]:
    """Reverses the result of json_stringify_champions"""
    champions = {}
    for championText in loads(championTexts):
        champion = parse_champion(championText)
        champions[champion.name] = champion
    return champions

def stringify_champion(champion: Champion) -> str:
    return ",".join(champion.str_tuple)

def json_stringify_champion(champions: dict[str, Champion]) -> str:
    """Takes a dictionary of champions and converts it to a stringified list of stringified champions"""
    return dumps([stringify_champion(c) for c in list(champions.values())])