import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# write server ip and port, and connect
#serverName = socket.gethostbyname(socket.gethostname())
#serverPort = 18881
client_socket.connect(('127.0.0.1',18881))

client_socket.send(b'GET /index.html HTTP/1.1\r\nHost: 127.0.0.1:18881\r\n\r\n')
response = client_socket.recv(4096)

client_socket.close()
print(response.decode())