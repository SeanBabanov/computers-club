import socket
import threading
import sqlite3

thread_local_db = threading.local()
clients = []

def get_db():
    thread_local_db.connection = sqlite3.connect('messages.db')
    return thread_local_db.connection

def handle_client(conn, addr):
    db = get_db()
    cursor = db.cursor()
    clients.append(conn) 
    print(f"Connected by {addr}")

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"Received message from {addr}: {message}")
            cursor.execute("INSERT INTO messages (client_address, message) VALUES (?, ?)", (addr[0], message))
            db.commit()
            for client in clients:
                if client != conn:
                    try:
                        client.sendall(data)
                    except:
                        clients.remove(client)
        except Exception as e:
            print(f"Exception occurred: {e}")
            break
    conn.close()
    clients.remove(conn)
    print(f"Connection with {addr} closed")

def start_server(host='localhost', port=12345):
    db = get_db()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server has started, listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
