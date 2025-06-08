#! python3

"""
Automated testing
Assignment: Chat with file transfers

1. Start the server program
2. Start client programs
3. Input data from standard input for the clients
4. Redirect standard output to files
5. Compare transferred files to original files

24 points total
"""

import os, time, subprocess
from file_compare import FileCompare
from within_file import WithinFile
points= 0
compare= FileCompare()
withinFile= WithinFile()

shell_command= 'cd client1; rm one-liners.txt'
os.system( shell_command )
shell_command= 'cd client2; rm Ameca_splendens.jpg'
os.system( shell_command )
shell_command= 'cd client3; rm Ameca_splendens.jpg'
os.system( shell_command )

print( 'Executing multiple messages between clients...' )

args= ['py','-u','ChatServer.py','6001']
server_errors= open( 'server-errors.txt', 'w' )
server= subprocess.Popen( args, stderr= server_errors )

time.sleep( 1 ) 

shell_command= 'cd client1; py ../input-writer-cmds-chat.py 1 3 5 client1-msgs.txt 2>errors.txt | py -u ../ChatClient.py -l 6002 -p 6001 >client1-recvd.txt 2>client1-errors.txt &'
os.system( shell_command )

shell_command= 'cd client2; py ../input-writer-cmds-chat.py 2 3 4 client2-msgs.txt 2>errors.txt | py -u ../ChatClient.py -l 6003 -p 6001 >client2-recvd.txt 2>client2-errors.txt &'
os.system( shell_command )

shell_command= 'cd client3; py ../input-writer-cmds-chat.py 3 3 3 client3-msgs.txt 2>errors.txt | py -u ../ChatClient.py -l 6004 -p 6001 >client3-recvd.txt 2>client3-errors.txt'
os.system( shell_command )

print( 'execution completed; grading...' )

subpoints= 0

found= withinFile.searchText( 'client1/client1-recvd-from-client2-multiple-ref.txt', 'client1/client1-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client1 did not recieve messages from client2' )

found= withinFile.searchText( 'client1/client1-recvd-from-client3-multiple-ref.txt', 'client1/client1-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client1 did not recieve messages from client3' )

found= withinFile.searchText( 'client2/client2-recvd-from-client1-multiple-ref.txt', 'client2/client2-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client2 did not recieve messages from client1' )

found= withinFile.searchText( 'client2/client2-recvd-from-client3-multiple-ref.txt', 'client2/client2-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client2 did not recieve messages from client3' )

found= withinFile.searchText( 'client3/client3-recvd-from-client1-multiple-ref.txt', 'client3/client3-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client3 did not recieve messages from client1' )

found= withinFile.searchText( 'client3/client3-recvd-from-client2-multiple-ref.txt', 'client3/client3-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client3 did not recieve messages from client2' )

points+= subpoints

server.kill()
try:
	server_errors.close()
except Exception:
	pass

print( 'Executing file transfers between clients...' )

args= ['py','-u','ChatServer.py','6001']
server_errors= open( 'server-errors.txt', 'w' )
server= subprocess.Popen( args, stderr= server_errors )

time.sleep( 1 ) 

shell_command= 'cd client1; py ../input-writer-cmds-chat.py 1 3 5 client1-file.txt 2>>errors.txt | py -u ../ChatClient.py -l 6002 -p 6001 >client1-recvd.txt 2>>client1-errors.txt &'
os.system( shell_command )

shell_command= 'cd client2; py ../input-writer-cmds-chat.py 2 3 5 client2-file.txt 2>>errors.txt | py -u ../ChatClient.py -l 6003 -p 6001 >client2-recvd.txt 2>>client2-errors.txt &'
os.system( shell_command )

shell_command= 'cd client3; py ../input-writer-cmds-chat.py 3 3 5 client3-file.txt 2>>errors.txt | py -u ../ChatClient.py -l 6004 -p 6001 >client3-recvd.txt 2>>client3-errors.txt'
os.system( shell_command )

print( 'execution completed; grading...' )

differ= compare.binFiles( 'client1/one-liners.txt', 'client2/one-liners.txt' )
if differ is False: 
	points+= 2
else:
	print( 'client1 did not recieve one-liners.txt' )

differ= compare.binFiles( 'client2/Ameca_splendens.jpg', 'client1/Ameca_splendens.jpg' )
if differ is False: 
	points+= 2
else:
	print( 'client2 did not receive Ameca_splendens.jpg' )

differ= compare.binFiles( 'client3/Ameca_splendens.jpg', 'client1/Ameca_splendens.jpg' )
if differ is False: 
	points+= 2
else:
	print( 'client3 did not receive Ameca_splendens.jpg' )

server.kill()
try:
	server_errors.close()
except Exception:
	pass

shell_command= 'cd client1; rm one-liners.txt'
os.system( shell_command )
shell_command= 'cd client2; rm Ameca_splendens.jpg'
os.system( shell_command )
shell_command= 'cd client3; rm Ameca_splendens.jpg'
os.system( shell_command )

print( 'Executing multiple message and file transfers between clients...' )

args= ['py','-u','ChatServer.py','6001']
server_errors= open( 'server-errors.txt', 'w' )
server= subprocess.Popen( args, stderr= server_errors )

time.sleep( 1 ) 

shell_command= 'cd client1; py ../input-writer-cmds-chat.py 1 3 5 client1-all.txt 2>>errors.txt | py -u ../ChatClient.py -l 6002 -p 6001 >client1-recvd.txt 2>>client1-errors.txt &'
os.system( shell_command )

shell_command= 'cd client2; py ../input-writer-cmds-chat.py 2 3 5 client2-all.txt 2>>errors.txt | py -u ../ChatClient.py -l 6003 -p 6001 >client2-recvd.txt 2>>client2-errors.txt &'
os.system( shell_command )

shell_command= 'cd client3; py ../input-writer-cmds-chat.py 3 3 5 client3-all.txt 2>>errors.txt | py -u ../ChatClient.py -l 6004 -p 6001 >client3-recvd.txt 2>>client3-errors.txt'
os.system( shell_command )

print( 'execution completed; grading...' )

subpoints= 0

found= withinFile.searchText( 'client1/client1-recvd-from-client2-multiple-ref.txt', 'client1/client1-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client1 did not recieve messages from client2' )

found= withinFile.searchText( 'client1/client1-recvd-from-client3-multiple-ref.txt', 'client1/client1-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client1 did not recieve messages from client3' )

found= withinFile.searchText( 'client2/client2-recvd-from-client1-multiple-ref.txt', 'client2/client2-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client2 did not recieve messages from client1' )

found= withinFile.searchText( 'client2/client2-recvd-from-client3-multiple-ref.txt', 'client2/client2-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client2 did not recieve messages from client3' )

found= withinFile.searchText( 'client3/client3-recvd-from-client1-multiple-ref.txt', 'client3/client3-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client3 did not recieve messages from client1' )

found= withinFile.searchText( 'client3/client3-recvd-from-client2-multiple-ref.txt', 'client3/client3-recvd.txt' )
if found:
	subpoints+= 1
else:
	print( 'client3 did not recieve messages from client2' )

points+= subpoints

differ= compare.binFiles( 'client1/one-liners.txt', 'client2/one-liners.txt' )
if differ is False: 
	points+= 2
else:
	print( 'client1 did not recieve one-liners.txt' )

differ= compare.binFiles( 'client2/Ameca_splendens.jpg', 'client1/Ameca_splendens.jpg' )
if differ is False: 
	points+= 2
else:
	print( 'client2 did not receive Ameca_splendens.jpg' )

differ= compare.binFiles( 'client3/Ameca_splendens.jpg', 'client1/Ameca_splendens.jpg' )
if differ is False: 
	points+= 2
else:
	print( 'client3 did not receive Ameca_splendens.jpg' )

server.kill()
try:
	server_errors.close()
except Exception:
	pass

print( 'Points: ' + str(points) );
