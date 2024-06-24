import socket
import threading

def receive_message(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print("Server:", message)
    client_socket.close()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_HOST = 'localhost'
    PORT = 12345
    client_socket.connect((SERVER_HOST, PORT))

    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("You: ")
        client_socket.sendall(message.encode())

        if message.lower() == 'exit':
            break
    client_socket.close()

if __name__ == "__main__":
    main()