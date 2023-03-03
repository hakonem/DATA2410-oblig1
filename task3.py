#import socket, thread and sys modules
from socket import *
import _thread as thread
import sys

#CLIENT HANDLER FUNCTION
#manages communication between each newly created connection socket and the server
def handleClient(connectionSocket):                         
    while True:
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
            print('thread closed')
            break                                           #prevents server socket from closing while other clients are still connected

        #EXCEPTION HANDLING
        except IOError:
            connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())    #if the file is not found, 404 message is returned instead
            connectionSocket.close()                                            #close client socket once message sent
            print('thread closed')
            break                                           #prevents closing server socket while other clients are still connected

#MAIN FUNCTION
#creates a main thread in which the server socket listens for new connection requests and spawns a new thread for each one
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)             #prepare a TCP (SOCK_STREAM) server socket using IPv4 (AF_INET)
    try:
        serverSocket.bind(('',18881))                       #bind server socket to local address ('' = all available addresses) and port
    #EXCEPTION HANDLING
    except:
        print('Bind failed. Error: ')                       #print error message and terminate program if socket binding fails 
        sys.exit()
    serverSocket.listen(10)                                 #listen for incoming connection requests to socket (no more than 10 at a time)
    print('Ready to serve...')                              #print message when socket ready to receive
    while True:
        connectionSocket,addr = serverSocket.accept()       #accept connection request from client and create new connection socket with info about the client (addr)
        print('Server connected by ',addr)                  #client info printed to screen server side
        thread.start_new_thread(handleClient,(connectionSocket,))       #start new thread and return its identifier
        print('new thread started')
    serverSocket.close()                                    #close server socket
    sys.exit()                                              #terminate the program after sending the corresponding data

if __name__ == '__main__':
    main()                                                  #execution of module begins with main()