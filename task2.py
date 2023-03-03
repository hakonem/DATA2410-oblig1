#import socket and sys modules
from socket import *
import sys

client_socket = socket(AF_INET, SOCK_STREAM)        #prepare a TCP (SOCK_STREAM) client socket using IPv4 (AF_INET)
client_socket.connect(('127.0.0.1',18881))          #connect client socket to specified server ip/port and initiate three-way handshake

print('Enter the IP address, port, and path to requested file, separated by spaces')          #prompt user for input in valid format

while True:
    input = sys.stdin.readline()                    #read user input (host port filename) and save in 'input' variable

    #input values need to be split up and inserted into a string to create valid GET request in format: GET <path to file> HTTP/1.1\r\nHost: <host>\r\n\r\n
    request = 'GET /' + input.split()[2] + ' HTTP/1.1\r\nHost: ' + input.split()[0] + ':' + input.split()[1] + '\r\n\r\n'
    client_socket.send(request.encode())            #send request to server
    print(client_socket.recv(1024).decode())        #receive response (max 1024 bytes) from server (header + file contents)

client_socket.close()                               #close client socket once GET response and file content is received