import sys, threading, socket, os, struct, time

global socket_closed
global user_input
global functionality_d

socket_closed = False
user_input = ""
functionality_d = { "message": "m", "file": "f", "exit": "x" }
clients_dict = {}
clients_empty = False

import socket
import threading
import sys

clients_dict = {}
socket_closed = False 
clients_empty = False

def receive(sock):
    global socket_closed
    global clients_empty

    try:
        receive_helper(sock)
    except:
        pass

    if sock in clients_dict:
        del clients_dict[sock]
        clients_empty = (len(clients_dict) == 0) 
        if clients_empty:
            sock.shutdown(socket.SHUT_WR)
            socket_closed = True
        
    sock.close() 

def receive_helper(sock):
    global clients_empty

    #firstname
    msg = []
    msg.append(sock.recv(1024).decode())
    first_name = msg[0]
    clients_dict[sock] = first_name
    clients_empty = False

    while True:
        bytes = sock.recv(1024).decode()
        if not bytes:
            break 

        #msg
        msg.append(bytes)
        msg_bytes = bytes

        chat = (first_name + ": " + msg_bytes + '\n')
        chat = chat.encode()

        #send to client(s)
        for key in clients_dict:
            if key != sock:
                key.send(chat)  

def server(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #restart
    serversocket.bind(('', port)) # binds to any available interface
    serversocket.listen(5) 
  
    #serversocket.close() # we have client, server no longer needed

    while True:
        sock, addr = serversocket.accept()
        mr_thready(sock)

def mr_thready(sock):
    threads = [] 

    receiver_thread = threading.Thread(target=receive, args=(sock,))

    threads.append(receiver_thread)
    
    receiver_thread.start()

    return threads

def usage( script_name ):
    print( 'Usage: py ' + script_name + ' <port number>' ) # print portnum (arg1 + arg2)


def main():
    argc = len(sys.argv)
    if argc != 2:
        usage(sys.argv[0])
        sys.exit()

    port = int(sys.argv[1])

    #server
    server(port)

if __name__ == "__main__":
    main()

