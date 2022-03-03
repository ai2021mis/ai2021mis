import socket
import select
import errno
import time
import sys

HEADERSIZE = 10
IP = "192.168.137.1"
PORT = 1234

#my_username = socket.gethostname()
my_username = '192.168.1.1'


while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)
        client_socket.connect((IP, PORT))
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
        #client_socket.setblocking(False)
        username = my_username.encode("utf-8")
        username_header = f"{len(username):<{HEADERSIZE}}".encode("utf-8")
        client_socket.send(username_header + username)
        connection_status = True
        print("Successfully connect to server")
        break

    except ConnectionRefusedError as e:
        #if e.errno == errno.WSAECONNREFUSED:
        print("A: connection closed by the server:")
        print("A: waiting for reconnect...")
        time.sleep(5)
        print("A: reconnecting...")

    except socket.timeout:
        print("A2: connection closed by the server:")
        print("A2: waiting for reconnect...")
        time.sleep(5)
        print("A2: reconnecting...")
        
    except Exception as e:
        print("General error:", str(e))
        sys.exit()


while True:

    try:
        while True:
            # receive things
            if connection_status:
                message = "heartbeat"
                #message ="live"
                message = message.encode("utf-8")
                message_header = f"{len(message):<{HEADERSIZE}}".encode("utf-8")
                client_socket.send(message_header + message)
                
                time.sleep(4)
                username_header = client_socket.recv(HEADERSIZE)
                if not len(username_header):
                    print("connection closed by the server:")
                    print("waiting for reconnect...")
                    connection_status = False
            else:
                print("C: connection closed by the server:")
                print("C: waiting for reconnect...")

            if connection_status:
                username_length = int(username_header.decode("utf-8").strip())
                username = client_socket.recv(username_length).decode("utf-8")

                message_header = client_socket.recv(HEADERSIZE)
                message_length = int(message_header.decode("utf-8").strip())
                message = client_socket.recv(message_length).decode("utf-8")

                print(f"{username} > {message}")

            else:
                time.sleep(5)
                print("reconnecting...")
                # sys.exit()
                client_socket.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(10)
                client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 15)
                client_socket.connect((IP, PORT))
                #client_socket.setblocking(False)
                username = my_username.encode("utf-8")
                username_header = f"{len(username):<{HEADERSIZE}}".encode("utf-8")
                client_socket.send(username_header + username)
                connection_status = True
                print("Successfully connect to server")

    except socket.timeout:
        print("C2: connection closed by the server:")
        print("C2: waiting for reconnect...")
        time.sleep(5)
        print("C2: reconnecting...")
        connection_status = False


    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            connection_status = False
            print('B: Reading error', str(e))
            

    except Exception as e:
        print("General error:", str(e))
        sys.exit()
