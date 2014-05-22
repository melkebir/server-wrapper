#!/usr/bin/python
import socket
import sys
import time
from messages import ClientMessage
from messages import ServerMessage
import messages
import os
 
if __name__ == "__main__":
    if len(sys.argv) == 3:
        name = sys.argv[1]
        port = int(sys.argv[2])
    else:
        name = "localhost"
        port = 9000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((name, port))
    while True:
        in_str = raw_input("> ")
        s = in_str.rstrip("\n").split(" ")

        if s[0] == "x":
            sock.close()
            break
        elif s[0] == "?":
            print "A client-to-server message is structured as follows."
            print "     __________________________________________________________"
            print "    |          |             |      |                |         |"
            print "    | type     | name_length | name | payload_length | payload |"
            print "    | (1 byte) | (4 bytes)   |      | (4 bytes)      |         |"
            print "    |__________|_____________|______|________________|_________|"
            print
            print "A server-to-client message is structured as follows."
            print
            print "     _____________________________________"
            print "    |          |                |         |"
            print "    | type     | payload_length | payload |"
            print "    | (1 byte) | (4 bytes)      |         |"
            print "    |__________|________________|_________|"
            print
            print
            print "These are the messages:"
            print
            print "| type | description           | direction |"
            print "|------|-----------------------|-----------|"
            print "| 00   | Alive?                | c -> s    |"
            print "| 08   | ACK                   | s -> c    |"
            print "| 09   | NACK                  | s -> c    |"
            print "| 10   | Regular parameter     | c -> s    |"
            print "| 20   | Input file parameter  | c -> s    |"
            print "| 30   | Output file parameter | c -> s    |"
            print "| 40   | Run                   | c -> s    |"
            print "| 50   | Get output            | c -> s    |"
            print "| 59   | Output                | s -> c    |"
        else:
            t = int(s[0])
            name = ""
            payload = ""
    
            if (len(s) > 1):
                name = s[1]
            if (len(s) > 2):
                if os.path.exists(s[2]):
                    with open(s[2], "rb") as f:
                        payload = bytearray(f.read())
                else:
                    payload = s[2]
    
            m = ClientMessage(t, len(name), name, len(payload), payload)
            m.send(sock)
            m = ServerMessage.receive(sock)
            print m.message_type, m.payload

