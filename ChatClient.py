# Final Version of ChatClient
import sys, threading, socket, os, struct, time
global socket_closed
global user_input
global functionality_d

socket_closed = False
user_input = ""
functionality_d = { "message": "m", "file": "f", "exit": "x" }

def wait_for_it(wait_time):
	time.sleep(wait_time)

def send_file( sock, file_size, file ): # PrimFTPd_bin.py
	print( 'File size is ' + str(file_size) )
	file_size_bytes= struct.pack( '!L', file_size )
	# send the number of bytes in the file
	sock.send( file_size_bytes )
	# read the file and transmit its contents
	while True:
		file_bytes= file.read( 1024 )
		if file_bytes:
			sock.send( file_bytes )
		else:
			break
	file.close()

def no_file( sock ): # PrimFTPd_bin.py
	zero_bytes= struct.pack( '!L', 0 )
	sock.send( zero_bytes )

def receive_file( sock, filename ): # PrimFTP_bin.py 
	# receive the file lines returned from the server
	file= open( filename, 'wb' )
	while True:
		file_bytes= sock.recv( 1024 )
		if file_bytes:
			file.write( file_bytes )
		else:
			break
	file.close()

def accept_file(sock, f_name):
	# receive the file size; if empty, exit // # PrimFTP_bin.py 
	file_size_bytes= sock.recv( 4 )
	if file_size_bytes:
		file_size= struct.unpack( '!L', file_size_bytes[:4] )[0]
		if file_size:
			receive_file(sock, f_name[1:])
		else:
			print('File does not exist or is empty')
	else:
		print('File does not exist or is empty')
		
	sock.close()

def f_server(sock, port, f_name): # PrimFTPd_text.py code
	global socket_closed

	if socket_closed:
		return

	# create a listening object // # PrimFTPd_text.py code
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind(('localhost', port)) 
	serversocket.listen(5)

		# 1. send
		# 2. accept
		# 3. filesize

	if f_name.strip():
		sock.send(f_name.encode()) # PrimFTP_text.py code
	else:
		return
	
	# wait for a connection and accept it // # PrimFTPd_bin.py 
	sock, addr = serversocket.accept() 
	accept_file(sock, f_name)

def decode_recv(sock):
	# receive the port number from the server // # PrimFTPd_bin.py
	msg_bytes = sock.recv(1024).decode()
	split_bytes = msg_bytes.split("\n")

	if split_bytes:
		grab_port = int(split_bytes[0])
	else:
		grab_port = 0

	return grab_port

def receive(sock): 
	port_recv = decode_recv(sock)
	global socket_closed

	try:
		receive_helper(sock, port_recv)
	except: # exceptions, lock maybe??
		pass 

	if not socket_closed:
		socket_closed = True 
		receive_SHUTDOWN(socket_closed, sock)
		sock.shutdown(socket.SHUT_RD)
		sock.close()


def receive_SHUTDOWN(socket_closed, sock):
	if socket_closed:
		socket_closed = True
		os._exit(0)

def receive_helper(sock, f_port):
	global user_input
	global functionality_d

	while True:
		bytes = sock.recv(1024).decode()
		if not bytes:
			break

		tag = bytes[0] 
		data = bytes[1:]
		
		if tag == functionality_d["message"]:
			#message main
			print(data)

		elif tag == functionality_d["file"]:
			#file main
			sock_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			sock_file.connect(("localhost", f_port)) 

			# check whether the file exists; if it does, send back the file size
			try:
				file_stat= os.stat( data ) 
				if file_stat.st_size:
					file= open( data, 'rb' )
					send_file( sock_file, file_stat.st_size, file )
				else:
					no_file( sock_file )
			except OSError:
				no_file( sock_file )

			sock_file.close()

		else:
			#this shouldn't happen
			print("Debug: This shouldn't be here.")

def client(port, address, connect_server_port): 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock.connect((address, connect_server_port)) 
	mr_thready(sock)

	try:
		send_usr = sys.stdin.readline().rstrip( '\n' ) 
		sock.send(send_usr.encode())
	except:
		sock.shutdown
		sock.close()
		return	
	
	wait_for_it(.5)
	ui(sock, port, "client") 

def server(port): # // reference echoServer.py
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #restart
	serversocket.bind(('', port)) # binds to any available interface
	serversocket.listen(5) # accept any connection requests (client, address aka localhost)
	sock, addr = serversocket.accept() # we have client, server no longer needed
	serversocket.close() 

	mr_thready(sock)
	wait_for_it(.5)

	try:
		send_port = f"{port}\n"
		sock.send(send_port.encode())
	except:
		sock.shutdown
		sock.close()
		return	
	
	ui(sock, port, "server") 

def ui(sock, port, side): 
	
	global user_input

	while True:
		print("Enter an option ('m', 'f', 'x'):")
		print("\t(M)essage (send)")
		print("\t(F)ile (request)")
		print("e(X)it")

		user_input = sys.stdin.readline().rstrip( '\n' )
		user_input = user_input.lower()

		if user_input == functionality_d["message"]: #message
			message = user_input
			print("Enter your message:") 
			message += sys.stdin.readline().rstrip( '\n' ) 
			sock.send(message.encode())

		elif user_input == functionality_d["file"]: #file
			filename = user_input 
			print(f"Which file do you want?\n")
			filename += sys.stdin.readline().rstrip( '\n' ) 
			f_server(sock, port, filename) 

		elif user_input == functionality_d["exit"]: #exit
			print("closing your sockets...goodbye")
			sock.shutdown(socket.SHUT_WR)
			sock.close()
			if not socket_closed:
				socket_closed = True
			sys.exit()

		else: 
			print ("This character was not valid. Please choose 'm', 'f', or 'x'!!!") 

		user_input = ""

def mr_thready(sock):
	threads = [] 
	
	receiver_thread = threading.Thread(target=receive, args=(sock,))

	threads.append(receiver_thread)

	receiver_thread.start()

	return threads

def usage( script_name ):
    print( 'Usage: py ' + script_name + ' <port number>' ) # print portnum (arg1 + arg2)

def main():
    # check args
    argc= len( sys.argv ) # check len of args, only possibilities are 3 for server, 5 or 7 for client
    choice = 5 # 0 for server, 1 for client

    if not (argc == 3 or argc == 5 or argc == 7): 
        usage(sys.argv[0])
        sys.exit(1)

    port = int(sys.argv[2])

    #1.
    # run as client or server based on CLI args
    # -l for server
    #if (argc == 3 and sys.argv[1] == '-l'):
    if (argc == 3):
        choice = 0

    #client
    # -s for address of server and -p for port number
    # if no -s, the program connects to local host
    elif (argc == 5 or argc == 7):
        #client
        choice = 1
        if (argc == 5 and sys.argv[3] == '-p'):
            #localhost
            address = 'localhost'
            connect_server_port = int(sys.argv[4])
        elif (argc == 7 and sys.argv[3] == '-s' and sys.argv[5] == '-p'):
            address = sys.argv[4]
            connect_server_port = int(sys.argv[6])

    if (choice == 0):
        #server
        server(port)
    elif (choice == 1):
        #client
        client(port, address, connect_server_port)
    else: # something went wrong
        sys.exit(1)


if __name__ == "__main__":
    main()