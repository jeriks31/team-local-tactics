from threading import Thread, activeCount
import socket

def _handleClient(connection:socket.socket, address:socket.AddressFamily):
    try:
        print(f"[{address}] Connected")
        while True:
            message = connection.recv(1024).decode("utf8").strip()
            if len(message) == 0:
                break
            print(f"[{address}] Message: {message}")

    except ConnectionError:
        # Most likely, the client application closed.
        print(f"[{address}] Connection error")
        
    finally:
        connection.close()
        print(f"[{address}] Disconnected")
    
if __name__ == "__main__":
    HOST = socket.gethostbyname(socket.gethostname())

    # Configure server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, 5522))
        server.listen()

        print(f"[Server] Started listening on {HOST}:{5522}")

        # Connection loop
        # while True:
        #     connection, address = server.accept()
        #     thread = Thread(target=_handle_client_connect, args=(connection, address))
        #     thread.start()
        while True:
            connection, address = server.accept()
            _handleClient(connection, address)

    print("[Server] Stopped")