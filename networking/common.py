from core import Champion
from json import dumps, loads

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
