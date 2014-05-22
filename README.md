Server-wrapper
==============

Protocol
--------

A client-to-server message is structured as follows.

     __________________________________________________________
    |          |             |      |                |         |
    | type     | name_length | name | payload_length | payload |
    | (1 byte) | (4 bytes)   |      | (4 bytes)      |         |
    |__________|_____________|______|________________|_________|

A server-to-client message is structured as follows.

     _____________________________________
    |          |                |         |
    | type     | payload_length | payload |
    | (1 byte) | (4 bytes)      |         |
    |__________|________________|_________|


These are the messages:

| type | description           | direction |
|------|-----------------------|-----------|
| 00   | Alive?                | c -> s    |
| 08   | ACK                   | s -> c    |
| 09   | NACK                  | s -> c    |
| 10   | Regular parameter     | c -> s    |
| 20   | Input file parameter  | c -> s    |
| 30   | Output file parameter | c -> s    |
| 40   | Run request           | c -> s    |
| 50   | Get output            | c -> s    |
| 59   | Output                | s -> c    |

Use-case scenario
=================

Preliminaries
-------------

1. Start server on port `9001` only allowing for `1` concurrent run request that writes input and output files in `/tmp` and executes the command `/ufs/elkebir/src/heinz/build/heinz`

2. Start client that connects to `localhost` via port `9001`



    ./server.py 9001 1 /tmp /ufs/elkebir/src/heinz/build/heinz
    ./testclient localhost 9001
    
    
Client-server communication
---------------------------
    
1. Do a ping:


