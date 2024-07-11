import socket
import threading

def receive_messages(s):
    while True:
            data = s.recv(1024)
            if not data:
                break
            print(f"Server: {data.decode()}")

def connect_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.start()

        while True:
            message = input("Enter message, to exit enter 'exit': ")
            if message == 'exit':
                break
            s.sendall(message.encode())

if __name__ == "__main__":
    connect_server()
