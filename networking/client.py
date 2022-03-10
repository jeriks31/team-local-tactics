from collections import Callable
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from core import Champion
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


def print_available_champs(champions: dict[str, Champion]) -> None:

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    print(available_champs)


def input_champion(prompt: str,
                   color: str,
                   champions: dict[str, Champion],
                   player1: list[str],
                   player2: list[str]) -> None:

    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        name = Prompt.ask(f'[{color}]{prompt}')
        if name not in champions: print(f'The champion {name} is not available. Try again.')
        elif name in player1: print(f'{name} is already in your team. Try again.')
        elif name in player2: print(f'{name} is in the enemy team. Try again.')
        else:
            player1.append(name)
            break
