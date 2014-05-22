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
| 39   | Output file name      | s -> c    |
| 40   | Run request           | c -> s    |
| 50   | Finished request      | c -> s    |
| 58   | Finished response     | s -> c    |
| 59   | Not finished response | s -> c    |
| 60   | Get output            | c -> s    |
| 69   | Output                | s -> c    |
