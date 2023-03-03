#import socket and sys modules
from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)             #prepare a TCP (SOCK_STREAM) server socket using IPv4 (AF_INET)
serverSocket.bind(('',18881))                           #bind server socket to local address ('' = all available addresses) and port
serverSocket.listen(1)                                  #listen for incoming connection requests to socket (no more than 1 at a time)
print('Ready to serve...')                              #print message when socket ready to receive

while True:
    connectionSocket,addr = serverSocket.accept()       #accept connection request from client and create new connection socket with info about the client (addr)
    try:
        message = connectionSocket.recv(1024)           #receive GET request from client (max 1024 bytes), save to 'message' variable

        #GET request arrives in following format: GET <path to file> HTTP/1.1\r\nHost: <host>\r\n\r\n
        
        filename = message.split()[1]                   #extract path to requested file (second element in request line), save to 'filename' variable
        f = open(filename[1:])                          #read path from second character (ignore initial '/'), save to 'f' variable
        outputdata = f.read()                           #read file and store contents in 'outputdata' variable
        f.close()                                       #close file

        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())       #if file is found, HTTP header line is sent to from connection socket to client
        connectionSocket.send(outputdata.encode() + '\r\n'.encode())    #contents of the requested file sent to the client 
        connectionSocket.close()                                        #close connection socket once HTML file is sent

    #EXCEPTION HANDLING
    except IOError:
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())     #if the file is not found, 404 message is returned instead
        connectionSocket.close()                                             #close client socket once message sent

serverSocket.close()                                    #close server socket
sys.exit()                                              #terminate the program after sending the corresponding data