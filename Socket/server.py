import socket, select
import time
import sys
import requests
import datetime


# HEADERSIZE = 10
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # print(socket.gethostname())
# s.bind((socket.gethostname(), 1236))
# s.listen(5)
#
# while True:
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} has been established!")
#     msg = "Welcome to the server!"
#     msg = f"{len(msg):<{HEADERSIZE}}" + msg
#     clientsocket.send(bytes(msg, "utf-8"))
#
#     while True:
#         time.sleep(3)
#         msg = f"Checking, {time.time()}"
#         msg = f"{len(msg):<{HEADERSIZE}}" + msg
#         clientsocket.send(bytes(msg, "utf-8"))


# msg = "Welcome to the server!"
# msg = f"{len(msg):<{HEADERSIZE}}" + msg
# msg = bytes(msg, "utf-8")
# print(msg)
# print("A:", int(msg[:HEADERSIZE].decode("utf-8")))
# print("B:", int(msg[:HEADERSIZE].decode("utf-8").strip()))

HEADERSIZE = 10
IP = "192.168.137.1"
PORT = 1234

ngrok_url = "http://afab-211-23-17-129.ngrok.io/"
jetson_url = ngrok_url + 'api/jetson/'
username = 'admin'
password = 'admin'

def time_now():
    time = datetime.datetime.now()
    time = time.strftime("%Y/%m/%d %H:%M:%S")
    return str(time)


def put_message(ip, status, timestamp_message):
    data = {
        'status': status,
        'timestamp': timestamp_message,
          }
    id = ip.replace('.','')
    aaa = requests.put(jetson_url + id +'/', data=data, auth=(username, password))
    print(aaa)


def push_message(ip, status, timestamp_message):
    data = {
        'ip' : ip,
        'status': status,
        'timestamp': timestamp_message,
          }
    aaa = requests.post(jetson_url, data=data, auth=(username, password))
    print(aaa)


##################################################

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERSIZE)
        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())    # skip header and counting the length of message
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, write_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:   # someone sent nothings
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            timestamp_message = 'CON:' + time_now()
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
            put_message(ip=user['data'].decode('utf-8'), status=0, timestamp_message=timestamp_message)

        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                timestamp_message = 'DIS:' + time_now()
                put_message(ip=clients[notified_socket]['data'].decode('utf-8'), status=1, timestamp_message=timestamp_message)
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f"Received message from {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}")
            notified_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            # for client_socket in clients:
            #     if client_socket != notified_socket:
            #         client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

            if message['data'].decode('utf-8') == 'bye':
                sys.exit()

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
