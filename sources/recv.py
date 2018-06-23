import socket

def recv(socket):
    try :
        return socket.recv()
    except:
        return None
