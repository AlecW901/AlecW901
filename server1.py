import socket
from threading import Thread


serv= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
host = ''
port = 1234
HEADER_SIZE=1024
ADDR=(host,port)

clients={}
addresses={}

serv.bind((ADDR))
serv.listen(5)
def accept_connections():
    while True:
        client, client_address= serv.accept()
        print("%s:%s has connected."%client_address)
        client.send(str.encode("Connection Established! Enter your name"))
        addresses[client]= client_address
        Thread(target=client_management, args=(client,)).start()

def client_management(client):
    name= client.recv(HEADER_SIZE).decode("utf8")
    welcome= 'Welcome %s! If you want to quit, type {.exit} to exit.' %name
    client.send(str.encode(welcome))
    msg= "%s has joined the chat!" % name
    broadcast(str.encode(msg))
    clients[client]=name

    while True:
        msg= client.recv(HEADER_SIZE)
        if msg!= str.encode("{.exit}"):
            broadcast(msg,name+": ")
        else:
            client.send(str.encode("{.exit}"))
            client.close()
            del clients[client]
            broadcast(str.encode("%s has left the chat." % name))
            break

def broadcast(msg,prefix=""):
    for s in clients:
        s.send(str.encode(prefix,)+msg)
def close():
    serv.shutdown(socket.SHUT_RDWR)
    serv.close()
if __name__=="__main__":
    serv.listen(5)
    print("Waiting for connections")
    ACCEPT_THREAD=Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    serv.close()
