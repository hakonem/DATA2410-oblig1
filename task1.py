#import socket module
from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a server socket
serverSocket.bind(('',18881))       #bind socket to server address and port
serverSocket.listen(1)              #listen for connection to socket
print('Ready to serve...')
while True:
    connectionSocket,addr = serverSocket.accept()       #accept new connection request from client
    try:
        message = connectionSocket.recv(4096)           #receive request message from client
        print(message)
        filename = message.split()[1]                   #extract path to requested object (second element in request line)
        f = open(filename[1:])                          #read path from second character (ignore initial '\')
        outputdata = f.read()                           #read file and store contents in outputdata
        f.close()                                       #close file

        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())    #Send one HTTP header line (if request successful) into socket

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send('\r\n'.encode())
        connectionSocket.close()

    except IOError:
            connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())     #Send response message for file not found

    connectionSocket.close()                #Close client socket
serverSocket.close()                        #Close server socket
sys.exit()                                  #Terminate the program after sending the corresponding data