import socket
import threading
import sqlite3

def save_message(client_address, message):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO messages (client_address, message) VALUES (?, ?)
    ''', (client_address, message))
    conn.commit()
    conn.close()

def handle_client(client_socket, client_address):
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print("Client:", message)
        client_socket.sendall(message.encode())
        save_message(client_address, message)
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 12345
    server_socket.bind(('localhost', PORT))
    server_socket.listen(5)
    print("Server is listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection established with", client_address)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address[0]))
        client_thread.start()

if __name__ == "__main__":
    main()