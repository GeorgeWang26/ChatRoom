import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = 'hello\n'.encode('utf-8')
print(type(msg))
client.sendto(msg, ('127.0.0.1', 6000))
print(client.recvfrom(1024))