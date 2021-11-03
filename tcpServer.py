import socket
import select

HOST = "0.0.0.0"
PORT = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set socket option of reuse address to 1
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)
print(socket.gethostbyname(socket.gethostname()))
connectionList = []
adrList = []
clientList = []

def terminateConnection(connection):
    print(connection)
    connection.close()
    for i in range(len(connectionList)):
        if connectionList[i] == connection:
            connectionList.pop(i)
            adrList.pop(i)
            print(connection, "\n============connection terminated============")
            return
    print('ERROR: cant find connection in clientList')

def directMessage(sender, msg):
    startIndex = msg.find('[')
    endIndex = msg.find(']')
    recieverIndex = int(msg[startIndex + 1 : endIndex])
    msg = msg[endIndex + 1 :]
    if recieverIndex >= len(connectionList):
        print("reciever not found for index:", recieverIndex, "  current max index:", len(connectionList)-1)
        return
    reciever = connectionList[recieverIndex]
    senderIndex = -1
    for i in range(len(connectionList)):
        if sender == connectionList[i]:
            senderIndex = i
            break
    text = "from user (" + str(senderIndex) + "): " + msg
    text = text.encode('utf-8')
    reciever.send(text)
    print('msg sent:', text)

def getCurrentUsers(con):
    response = "online users:\n"
    for i in range(len(connectionList)):
        response = response + str(i) + "\n"
    response = response.encode("utf-8")
    con.send(response)
    print("sent current users list")



try:
    print("server started on port", PORT)
    while True:
        redable, writable, execptional = select.select([server], [], [], 0)
        if redable:
            # print("waiting for connection")
            con, adr = server.accept()
            connectionList.append(con)
            adrList.append(adr)
            print('connection from:', adr, '   con:', con, '   current connection count:', len(connectionList))
        
        redable, writable, execptional = select.select(connectionList, [], [], 0)
        if redable:
            for connection in redable:
                # print("waiting for msg")
                msg = connection.recv(1024)
                msg = msg.decode('utf-8')
                # print(len(msg), len("CURRENT-USERS\r\n"))
                # print(msg=="CURRENT-USERS\r\n")
                if msg == "":
                    terminateConnection(connection)
                elif msg[0:4] == "P2P[":
                    directMessage(connection, msg)
                elif msg == "CURRENT-USERS\r\n":
                    getCurrentUsers(connection)
                else:
                    printMsg = "msg: " + msg + "from: "
                    print(printMsg, connection)
                    response = "msg recieved: " + msg
                    response = response.encode("utf-8")
                    connection.send(response)
except KeyboardInterrupt:
    for i in connectionList:
        i.close()
    server.shutdown()
    server.close()
    print("SERVER TERMINATED BY USER")