# Final working draft

import socket
import threading
import sys
import select
import os
stopThreads = threading.Event() 

def receiveMessage(clientSocket):
    while not stopThreads.is_set():  
        try:
            ready, _, _ = select.select([clientSocket], [], [], 60)
            if ready:
                message = clientSocket.recv(1024).decode()
                if message.startswith("FILE:"):
                    filename = message.split(":", 1)[1]
                    print("in receive messages")
                    receive_file(clientSocket, filename)
                if message == "shutdown":
                    stopThreads.set()  
                    break
                if not message:
                    print("No message received, possibly disconnected.")
                    stopThreads.set()  
                    break
                print(message)
            else:
                print("Receive timeout reached, shutting down for inactivity!")
                stopThreads.set()  
                break
        except Exception as e:
            print(f"Error in receiveMessages: {e}")
    clientSocket.close()
    sys.exit("Disconnected from server due to receive error or shutdown command.")

def receive_file(clientSocket, filename):
    file= open(filename, 'wb' )
    while True:
        print("receiving bytes")
        file_bytes= clientSocket.recv(1024)
        if file_bytes:
            file.write( file_bytes )
        else:
            break
    file.close()
    
def startClients(portNum):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSocket.settimeout(0.25)
    try:
        clientSocket.connect(("127.0.0.1", portNum))
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        sys.exit(1)

    # ask user for name and send its to server 
    nameOfClient = input("What is your name?\n").strip() 
    clientSocket.send(nameOfClient.encode("utf-8"))     # convert string to bytes using UTF-8 encoding                                                                            
    print("Sending name to server...")

    # Start the thread to listen for messages
    receive = threading.Thread(target=receiveMessage, args=(clientSocket,))
    receive.start()

    while True:  # Check if shutdown has been signaled
##        try: 
        print("Enter an option ('m', 'f', 'x'):")
        print("  (M)essage (send)")
        print("  (F)ile (request)")
        print(" e(X)it")
        selection = input().strip()
        if selection == 'm':
            print("Enter your message: ") 
            message = input().strip()
            clientSocket.send(f"MSG:{message}".encode("utf-8"))
            if message == "shutdown" or message == "exit":
                clientSocket.send("shutdown".encode("utf-8"))
                stopThreads.set()  
                break
        elif selection == 'f':
            print("Who owns the file?")
            file_owner = input().strip()
            print("Which file do you want?")
            filename = input().strip()
            clientSocket.send(f"FILE:{file_owner}/{filename}".encode("utf-8"))
            print("test" + filename)
            #receive_file(clientSocket, filename) # causing errors, filename is not defined
            print("test2")
        elif selection == 'x':
            print('closing your sockets...goodbye')
            stopThreads.set()
            clientSocket.shutdown(socket.SHUT_WR)
            clientSocket.close()
            os._exit(0)
        else:
            print("Invalid option...please pick again")
            continue
##        except Exception as e:
##            print(f"Error during send or input handling: {e}")
##            stopThreads.set() 
##            break

    receive.join()  

if __name__ == "__main__":
    portNum = int(sys.argv[4])
    startClients(portNum)