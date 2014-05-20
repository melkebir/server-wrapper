Server-wrapper
==============

Protocol
--------

A client-to-server message is structured as follows.

     _______________________________________________________
    |       |             |      |                |         |
    | type  | name_length | name | payload_length | payload |
    | (int) | (int)       |      | (int)          |         |
    |_______|_____________|______|________________|_________|

A server-to-client message is structured as follows.

     __________________________________
    |       |                |         |
    | type  | payload_length | payload |
    | (int) | (int)          |         |
    |_______|________________|_________|


These are the messages:

| type | description           | direction |
|------|-----------------------|-----------|
| 10   | Regular parameter     | c -> s    |
| 20   | Input file parameter  | c -> s    |
| 30   | Output file parameter | c -> s    |
| 39   | Output file name      | s -> c    |
| 40   | Run request           | c -> s    |
| 50   | Finished request      | c -> s    |
| 59   | Not finished response | s -> c    |
| 58   | Finished response     | s -> c    |
| 60   | Get output            | c -> s    |
| 69   | Output                | s -> c    |
