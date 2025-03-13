import socket
import os
import userportfind

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001
User_port_list = []

print('Starting up on {} port {}'.format(server_address,server_port))

sock.bind((server_address,server_port))

while True:
    try:
        header = sock.recv(9)

        Username_length = int.from_bytes(header[:1],"big")
        Message_length = int.from_bytes(header[1:5],"big")
        User_port = int.from_bytes(header[5:9],"big")
        if not userportfind.userportfind(User_port,User_port_list):
            User_port_list.append(User_port)
        else:
            pass

        print('Username-list: {}'.format(User_port_list))

        stream_rate = 4096

        print('Received header from client. User length {}, Data Lenght {} User port {}'.format(Username_length, Message_length, User_port))

        if Message_length == 0:
            raise Exception('No message to chat from client.')

        Username = sock.recv(Username_length).decode('utf-8')

        print('Username: {}'.format(Username))

        Message_bytes = sock.recv(Message_length)
        Message = Message_bytes.decode('utf-8')

        print('Message: {}'.format(Message))

        userportfind.sendmessage(sock,Message_bytes,server_address,User_port,User_port_list)

    except Exception as e:
        print('Error: ' + str(e))
    
    finally:
        print("Press enterKey")

