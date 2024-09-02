import socket
from threading import Thread

host=input('Enter host: ')
port=input('Enter port:')
if not port:
    port=1234
else:
    port=int(port)

BUFSIZ=1024
ADDR=(host,port)
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(ADDR)
def receive():
    while True:
        msg=client_socket.recv(BUFSIZ).decode("utf8")
        if msg=="{.exit}":
            client_socket.close()
            break
        if not msg:
            break
        print(msg)

def send():
    while True:
        msg=input()
        client_socket.send(str.encode(msg))
        if msg=="{.exit}":
            break

receive_thread=Thread(target=receive)
send_thread=Thread(target=send)
receive_thread.start()
send_thread.start()
receive_thread.join()
send_thread.join()