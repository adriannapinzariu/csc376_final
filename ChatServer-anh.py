#Final working draft

import socket
import threading
import os
import sys

listOfClients = []  # List of all client connections

threadLock = threading.Lock()

def broadcast(message, senderSocket):
    with threadLock:
        for client in listOfClients:
            if client != senderSocket:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"Failed to send message to a client: {e}")
                    client.close()
                    listOfClients.remove(client)

def send_file(clientSocket, file_path):
    """Send a file to a client."""
    file = open(file_path, 'rb')
    while True:
        file_bytes= file.read( 1024 )
        print("sending bytes")
        if file_bytes:
            clientSocket.send( file_bytes )
        else:
            break
    file.close()

def no_file( sock ):
    zero_bytes= struct.pack( '!L', 0 )
    sock.send( zero_bytes )
	

def handleClient(clientSocket):
    try:
        name = clientSocket.recv(1024).decode("utf-8")
        welcome_message = f"{name} has joined the chat!"
        broadcast(welcome_message.encode("utf-8"), clientSocket)
        while True:
            selection = clientSocket.recv(1024).decode("utf-8")
            if selection.startswith("MSG:"):
                #message = clientSocket.recv(1024).decode("utf-8")
                message = selection.split(":", 1)[1]
                formatted_message = f"{name}: {message}".encode("utf-8")
                broadcast(formatted_message, clientSocket)
            elif selection.startswith("FILE:"):
                file_path = selection.split(":", 1)[1]
                print(file_path)
                file_owner = file_path.split("/",1)[0]
                filename = file_path.split("/",1)[1]
                file_path = os.path.join(file_owner, filename)
                print ("In server: file path is " + file_path)
                clientSocket.send(f"FILE:{filename}".encode())
                send_file(clientSocket, file_path)
    finally:
        with threadLock:
            if clientSocket in listOfClients:
                listOfClients.remove(clientSocket)
        clientSocket.close()
        farewell_message = f"{name} has left the chat!"
        broadcast(farewell_message.encode("utf-8"), None)

def startServer(portNum):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    serverSocket.bind(("0.0.0.0", portNum))
    serverSocket.listen()
    print(f"Server started on port {portNum}")
     
    while True:
        clientSocket, _ = serverSocket.accept()
        with threadLock:
            listOfClients.append(clientSocket)
        threading.Thread(target=handleClient, args=(clientSocket,)).start()
        
if __name__ == "__main__":
    import sys
    portNum = int(sys.argv[1])
    startServer(portNum)