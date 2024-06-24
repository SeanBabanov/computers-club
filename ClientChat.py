import socket

def connect_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            message = input("Enter message, to exit enter 'exit': ")
            if message == 'exit':
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Server: {data.decode()}")

if __name__ == "__main__":
    connect_server()
