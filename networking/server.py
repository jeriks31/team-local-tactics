from collections.abc import Callable
from random import randint as generateClientId
from core import Match, Team, Champion
from storage import load_champions
import socket
import threading
import common

connections: list[tuple[socket.socket, str]] = []


def _handle_client(connection: socket.socket, address:socket.AddressFamily, onClientMessage:Callable[[int, str, list[str]], str]):
    # Help application identify client id
    _clientId = generateClientId(0, 9999)

    try:
        print(f"[{address[0]}] Connected")

        # Let game know client has connected
        onClientMessage(_clientId, common.MSG_CONNECT, [])

        # Handle connection messages
        while True:
            request = connection.recv(common.MSG_SIZE).decode("utf8").split(sep=common.MSG_CMD_SEP)
            print(f"[{address[0]}] '{request}'")

            message, args = (request[0], request[1].split(sep=common.MSG_ARG_SEP)) if len(request) > 1 else (request[0], []) 
            if request[0] == common.MSG_DISCONNECT: break
            response = onClientMessage(_clientId, message, args)
            connection.send(response.encode("utf8"))

    except ConnectionError:
        print(f"[{address[0]}] Connection closed unexpectedly")
    finally:
        connection.close()
        onClientMessage(_clientId, common.MSG_DISCONNECT, [])
        print(f"[{address[0]}] Disconnected")


def start(onClientMessage: Callable[[int, str, list[str]], str]) -> None:
    HOST = "localhost"

    # Configure server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, common.PORT))
        server.listen()

        print(f"[Server] Started on {HOST}:{common.PORT}")
        
        # Handle connection requests
        while True:
            connection, address = server.accept()
            connections.insert((connection, address))
            if len(connections) >= 2:
                rungame()

            # Handle connection single threaded
            # _handle_client(connection, address, onClientMessage)

            # Handle connection multi threaded
            # thread = threading.Thread(target=_handle_client, args=(connection, address, onClientMessage))
            # thread.start()


def rungame() -> None:
    champions = load_champions()

    stringified_champions = [common.stringify_champion(c) for c in champions.values()]
    for conn, addr in connections:
        conn.send("INITIAL_PRINTS" + common.MSG_CMD_SEP + common.MSG_ARG_SEP.join(stringified_champions))  # Tell clients to print the welcome msg and available champions

    player1 = []
    player2 = []

    # Champion selection
    for _ in range(2):
        requestChampionPick(connections[0][0], champions, player1, player2)
        requestChampionPick(connections[1][0], champions, player2, player1)

    # Match
    match = Match(
        Team("Red", [champions[name] for name in player1]),
        Team("Red", [champions[name] for name in player2])
    )
    match.play()

    for conn, addr in connections:
        conn.send(match) #Tell client to print match summary

def requestChampionPick(conn, champions, self_chosen, enemy_chosen) -> None:
    pass
