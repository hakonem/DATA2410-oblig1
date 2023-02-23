import socket
import sys
import requests

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# write server ip and port, and connect
#serverName = socket.gethostbyname(socket.gethostname())
#serverPort = 18881
client_socket.connect(('127.0.0.1',18881))

while True:
    url = "http://192.168.50.207:18881/index.html"
    request = requests.request("GET", url)
    #client_socket.send(b"GET / HTTP/1.1\r\nHost:192.168.50.207\r\n\r\n")
    response = client_socket.recv(2048)

client_socket.close()
print(response.decode())