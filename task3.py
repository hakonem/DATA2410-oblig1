from socket import *
import _thread as thread
import time
import sys

def now():
    return time.ctime(time.time())      #returns time of day

def handleClient(connectionSocket):               #client handler function
    while True:
        try:
            message = connectionSocket.recv(4096)           #receive request message from client
            print(message.decode())
            filename = message.split()[1]                   #extract path to requested object (second element in request line)
            f = open(filename[1:])                          #read path from second character (ignore initial '\')
            outputdata = f.read()                           #read file and store contents in outputdata
            print(outputdata)
            f.close()                                       #close file

            connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())    #Send one HTTP header line (if request successful) into socket

            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send('\r\n'.encode())
            connectionSocket.close()
            print('thread closed')
            break

        except IOError:
            connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())     #Send response message for file not found
            connectionSocket.close()
            print('thread closed')
            break

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('',18881)) 
    except:
        print('Bind failed. Error: ')
        sys.exit()
    serverSocket.listen(10)
    print('Ready to serve...')
    while True:
        connectionSocket,addr = serverSocket.accept()       #accept new connection request from client
        print('Server connected by ',addr)
        print('at ', now())
        thread.start_new_thread(handleClient,(connectionSocket,))
        print('new thread started')
    serverSocket.close()                        #Close server socket
    sys.exit()                                  #Terminate the program after sending the corresponding data

if __name__ == '__main__':
    main()