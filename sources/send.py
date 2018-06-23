import socket

def broadcast(message, socket_list, server_socket):
    if message==None:
        print("Cannot send an empty message.")
    else :
        for s in socket_list:
            s.send(message)

def send_one_user(message, usr_socket):
    if message==None:
        print("Cannot send an empty message.")
    else :
        try:
            usr_socket.send(message)
        except:
            print("Cannot send the message.")


if __name__ == "__main__":
    print("This is not an executable main file")
