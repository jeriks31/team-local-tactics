from collections.abc import Callable
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from core import Champion
import json
import common
import socket

_connection: socket.socket = None
msg_welcome = '\nWelcome to [bold yellow]Team Local Tactics[/bold yellow]!\nEach player choose a champion each time.\n'


def connect() -> None:
    """Connects to the server. If server is connected, the previous connection is disconnected."""
    global _connection
    if _connection is not None:
        disconnect()

    HOST = "localhost"
    _connection =  common.new_connection()
    _connection.connect((HOST, common.PORT))
    while True:
        handleMessage()

def handleMessage():
    global _connection
    message, args = common.receive_message(_connection)

    if message == common.MSG_MATCH_STARTED:
        print(msg_welcome)
        champions = common.json_parse_champions(args[0])
        print_available_champs(champions)
    elif message == common.MSG_PICK_CHAMPION:
        champions = common.json_parse_champions(args[0])
        self_chosen = json.loads(args[1])
        enemy_chosen = json.loads(args[2])
        input_champion(champions, self_chosen, enemy_chosen)


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


def input_champion(champions: dict[str, Champion],
                   self_chosen: list[str],
                   enemy_chosen: list[str]) -> None:
    global _connection
    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        name = Prompt.ask(f'[blue]Pick Champion')
        if name not in champions: print(f'The champion {name} is not available. Try again.')
        elif name in self_chosen: print(f'{name} is already in your team. Try again.')
        elif name in enemy_chosen: print(f'{name} is in the enemy team. Try again.')
        else:
            common.send_message(_connection, common.MSG_PICKED_CHAMPION, [name])
            break
