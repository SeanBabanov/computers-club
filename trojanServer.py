import socket
import ssl
import os
import mysql.connector
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_aes_key():
    return os.urandom(16)

def save_key_to_db(secret_key):
    connection = mysql.connector.connect(
        host='localhost',
        user='your_user',
        password='your_password',
        database='encrypted_files_db'
    )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO keys (secret_key) VALUES (%s)", (secret_key,))
    connection.commit()
    cursor.close()
    connection.close()

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9999))
server_socket.listen(5)
secure_socket = context.wrap_socket(server_socket, server_side=True)

while True:
    client_socket, addr = secure_socket.accept()
    secret_key = generate_aes_key()
    save_key_to_db(secret_key)
    client_socket.send(secret_key)
    client_socket.close()
