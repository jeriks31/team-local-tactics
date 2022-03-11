from core import Match, Team, Champion
from storage import load_champions
import json
import socket
import networking as net
import parsing

def start() -> None:
    """Starts the server."""
    HOST = "localhost"

    # Configure server
    with net.new_connection() as server:
        server.bind((HOST, net.PORT))
        server.listen()

        print(f"[Server] Started on {HOST}:{net.PORT}")
        

        # Handle connection requests
        while True:
            connections: list[tuple[socket.socket, str]] = []
            for _ in range(2):
                connection, address = server.accept()
                connections.append((connection, address))
            play_game(connections[0], connections[1])


def play_game(player1:tuple[socket.socket, str], player2:tuple[socket.socket, str]) -> None:
    """Plays a game. Requires two connected players."""

    print(f"[Server] Game started: {player1[1]} vs {player2[1]}")

    champions = load_champions()
    print(f"[Server] Loaded {len(champions)} champions")

    net.send_message(player1[0], net.MSG_MATCH_STARTED, [parsing.serialize_champions(champions)])
    net.send_message(player2[0], net.MSG_MATCH_STARTED, [parsing.serialize_champions(champions)])

    print(f"[Server] Players have been notified: Match has started")
    print(f"[Server] Picking champions")

    player1_champions = []
    player2_champions = []

    # Champion selection
    for _ in range(2):
        requestChampionPick(player1, champions, player1_champions, player2_champions)
        requestChampionPick(player2, champions, player2_champions, player1_champions)

    print(f"[Server] All champions have been picked")
    print(f"[Server] Match is starting")

    # Match
    match = Match(
        Team("Red", [champions[name] for name in player1_champions]),
        Team("Blue", [champions[name] for name in player2_champions])
    )
    match.play()

    player1_score, player2_score = match.score()
    
    print(f"[Server] Match is done. Score: ('{player1[1]}':{player1_score}) ('{player2[1]}':{player2_score})")

    net.send_message(player1[0], net.MSG_MATCH_ENDED, [player1_score, player2_score])
    net.send_message(player2[0], net.MSG_MATCH_ENDED, [player2_score, player1_score])

    print(f"[Server] Players have been notified: Match is ended")

    player1[0].close()
    player2[0].close()

def requestChampionPick(client:tuple[socket.socket, str], champions:list[Champion], self_chosen:list[Champion], enemy_chosen:list[Champion]) -> None:
    conn, addr = client

    # Let client pick champion
    _champions = parsing.serialize_champions(champions)
    _self_chosen = json.dumps(self_chosen)
    _enemy_chosen = json.dumps(enemy_chosen)
    net.send_message(conn, net.MSG_PICK_CHAMPION, [_champions, _self_chosen, _enemy_chosen])
    print(f"[Server] '{addr}' is picking a champion")

    # Handle client picked champion
    message, args = net.receive_message(conn)
    if message != net.MSG_PICKED_CHAMPION: raise f"Unexpected message from client: {message}"
    if len(args) != 1: raise f"Unexpected number of arguments from client. Expected 1, but was {len(args)}"
    champion_name = args[0]
    self_chosen.append(champion_name)
    print(f"[{addr}] Picked champion: {champion_name}")
