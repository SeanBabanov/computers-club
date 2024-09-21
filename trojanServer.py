import socket
import ssl

def create_ssl_server_socket(certfile, keyfile, host='0.0.0.0', port=8443):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket, context

def handle_client(ssl_socket):
    data = ssl_socket.recv(1024).decode('utf-8')
    ssl_socket.send("Hello, secure client".encode('utf-8'))

def run_ssl_server(certfile, keyfile, host='0.0.0.0', port=8443):
    server_socket, context = create_ssl_server_socket(certfile, keyfile, host, port)
    print("Waiting for clients...")

    while True:
        client_socket, addr = server_socket.accept()
        with context.wrap_socket(client_socket, server_side=True) as ssl_socket:
            handle_client(ssl_socket)
        client_socket.close()

run_ssl_server("server.crt", "server.key")