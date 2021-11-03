import socket
import select

server_addr = ("0.0.0.0", 6000)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_addr)

while True:
    redable, writable, execptional = select.select([server], [], [], 0)
    print("1")
    if redable:
        msg, adr = redable[0].recvfrom(1024)
        print(type(msg), msg, '   from:', adr)
        
        server.sendto('msg recieved\n'.encode('utf-8'), adr)