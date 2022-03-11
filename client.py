from rich import print
from rich.prompt import Prompt, Confirm
from rich.table import Table
from core import Champion, Match
import json
import networking as net
import socket
import parsing

msg_welcome = '\nWelcome to [bold yellow]Team Local Tactics[/bold yellow]!\nEach player choose a champion each time.\n'

def connect() -> None:
    """Connects to the server. If server is connected, the previous connection is disconnected."""
    HOST = "localhost"
    connection = net.new_connection()
    connection.connect((HOST, net.PORT))
    while True:
        handleMessage(connection)

def handleMessage(connection:socket.socket):
    message, args = net.receive_message(connection)

    if message == net.MSG_IDENTIFY:
        default = args[0]
        identify(connection, default)

    elif message == net.MSG_ENEMY_IDENTITY:
        name = args[0]
        show_enemy_name(name)

    elif message == net.MSG_MATCH_STARTED:
        print(msg_welcome)
        champions = net.parse_champions(args[0])
        show_champions(champions)

    elif message == net.MSG_PICK_CHAMPION:
        champions = net.parse_champions(args[0])
        self_chosen = json.loads(args[1])
        enemy_chosen = json.loads(args[2])
        pick_champion(connection, champions, self_chosen, enemy_chosen)

    elif message == net.MSG_MATCH_ENDED:
        self_name = args[0]
        match = json.loads(args[1], cls=Match)

def identify(connection: socket.socket, default:str) -> None:
    name = Prompt.ask(f'[blue]Pick a nickname', default=default, show_default=True)
    net.send_message(connection, net.MSG_IDENTIFY, [name])

def show_enemy_name(name:str):
    print(f"[bold red] Your enemy is: {name}")

def show_champions(champions: dict[str, Champion]) -> None:
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

def pick_champion(connection: socket.socket,
                   champions: dict[str, Champion],
                   self_chosen: list[str],
                   enemy_chosen: list[str]) -> None:
    # Prompt the player to choose a champion and provide the reason why
    # certain champion cannot be selected
    while True:
        name = Prompt.ask(f'[blue]Pick Champion')
        if name not in champions: print(f'The champion {name} is not available. Try again.')
        elif name in self_chosen: print(f'{name} is already in your team. Try again.')
        elif name in enemy_chosen: print(f'{name} is in the enemy team. Try again.')
        else:
            net.send_message(connection, net.MSG_PICKED_CHAMPION, [name])
            break

def show_match_result(self_name:str, match:Match):
    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column(match.red_team.name,
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column(match.blue_team.name,
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'{match.red_team.name}: {red_score}\n'
          f'{match.blue_team.name}: {blue_score}')

    # Print the winner
    messageWin = '\n[green]You won! :grin:'
    messageLoose = '\n[red]You lost... :grin:'

    if red_score == blue_score:
        print('\nDraw :expressionless:')
        return
    redWon = red_score > blue_score
    isRed = self_name == match.red_team.name
    message = messageWin if isRed and redWon or (not isRed) and (not redWon) else messageLoose
    print(message)

if __name__ == "__main__":
    connect()