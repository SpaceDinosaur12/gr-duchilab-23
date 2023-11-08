import socket

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 9999))
server_socket.listen()
print("Server is up and running")

(client_socket, client_address) = server_socket.accept()
print("Client connected")

while True:
    d = input()
    client_socket.send(d.encode())

client_socket.close()
server_socket.close()