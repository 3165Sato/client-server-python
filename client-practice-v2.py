import socket
import sys
import os
import threading
import userportfind

def protocol_header(Username_length, Message_length, User_port):
    return Username_length.to_bytes(1, "big") + Message_length.to_bytes(4,"big") + User_port.to_bytes(4,"big")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = input("Type in the server's address to connect to: ")
port = input("Type in the server's port to connect to: ")
server_port = 9001

print('connecting to {}'.format(server_address, port))

try:
    sock.bind((server_address,int(port)))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    username = input('Type in a UserName to access: ')
    username_bits = username.encode('utf-8')
except socket.error as err:
    print(err)
    sys.exit(1)

while True:
    try:
        message = input('Type in a Message to chat: ')
        message_bits = message.encode('utf-8')

        header = protocol_header(len(username_bits), len(message_bits), int(port))

        sock.sendto(header,(server_address,server_port))
        sock.sendto(username_bits,(server_address,server_port))
        sock.sendto(message_bits,(server_address,server_port))

        thread = threading.Thread(target=userportfind.recv_server, args=(sock,server_address))
        thread.start()
        # userportfind.recv_server(sock, server_address)

    finally:
        print('End socket')
        # sock.close()