import socket

if __name__ == "__main__":
    HOST = "192.168.86.36"
    PORT = 5522

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        while True:
            message = input("Send:").strip()
            client.send(message.encode("utf8"))
            if len(message) == 0:
                break
        print(f"Disconnected from {HOST}:{PORT}")
