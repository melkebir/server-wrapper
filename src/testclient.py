#!/usr/bin/python
import socket
import sys
import time
from messages import ClientMessage
import messages
 
if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9000))
    m = ClientMessage(messages.CLIENT_MESSAGE_REGULAR_PARAMETER, len(sys.argv[1]), sys.argv[1], len(sys.argv[2]), sys.argv[2])
    m.send(sock)
    m.send(sock)
    m.send(sock)
    time.sleep(2)
    m.send(sock)
    m.send(sock)
    sock.close()
