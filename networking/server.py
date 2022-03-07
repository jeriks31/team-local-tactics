from collections import Callable
from random import randint as genereateClientId
import socket
import threading
import common

def _handle_client(connection:socket.socket, address:socket.AddressFamily, onClientMessage:Callable[[int, str, list[str]], str]):
    # Help application identify client id
    _clientId = genereateClientId(0, 9999)

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

def start(onClientMessage:Callable[[int, str, list[str]], str]) -> None:
    HOST = "localhost"

    # Configure server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, common.PORT))
        server.listen()

        print(f"[Server] Started on {HOST}:{common.PORT}")
        
        # Handle connection requests
        while True:
            connection, address = server.accept()

            # Handle connection single threaded
            _handle_client(connection, address, onClientMessage)

            # Handle connection multi threaded
            # thread = threading.Thread(target=_handle_client, args=(connection, address, onClientMessage))
            # thread.start()