import socket
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# write server ip and port, and connect
#serverName = socket.gethostbyname(socket.gethostname())
#serverPort = 18881
client_socket.connect(('127.0.0.1',18881))

while True:
    input = sys.stdin.readline()              #input command format: host port filename
    #request = 'GET /index.html HTTP/1.1\r\nHost: 127.0.0.1:18881\r\n\r\n'
    request = 'GET /' + input.split()[2] + ' HTTP/1.1\r\nHost: ' + input.split()[0] + ':' + input.split()[1] + '\r\n\r\n'
    print(request)
    client_socket.send(request.encode())
    response = client_socket.recv(4096)
    client_socket.close()
    print(response.decode())