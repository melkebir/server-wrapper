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

* Start server on port `9001` only allowing for `1` concurrent run request that writes input and output files in `/tmp` and executes the command `/ufs/elkebir/src/heinz/build/heinz`

        `./server.py 9001 1 /tmp /ufs/elkebir/src/heinz/build/heinz`

* Start client that connects to `localhost` via port `9001`

        `./testclient localhost 9001`
    
    
Client-server session
---------------------
    
1. Do a ping:

        > 0
        8

  The server responds with `ACK (8)`.
  
2. Send over regular parameter `-p` 

        > 10 -p
        8
  
  The server responds with `ACK (8)`.

3. Send over regular parameter `-t 5` 

        > 10 -t 5
        8
  
  The server responds with `ACK (8)`.

4. Send over input file parameter `-n <FILE>`

        > 20 -n /ufs/elkebir/src/NINA/data/MWCS/test/nodes-from-russia.txt
        8
        
   The server responds with ACK (8) and generated a new file in the specified `/tmp` directory. The contents of this file correspond to `nodes-from-russia.txt`.

5. Send over input file parameter `-e <FILE>`

        > 20 -e /ufs/elkebir/src/NINA/data/MWCS/test/edges-from-russia.txt
        8

   The server responds with `ACK (8)` and generated a new file in the specified `/tmp` directory. The contents of this file correspond to `edges-from-russia.txt`.
   
6. Send over output file parameter `-o`

        > 30 -o
        8
       
   The server responds with `ACK (8)` and generated a new parameter `-o <NEW_OUT_FILE>` where `<NEW_OUT_FILE>` is a new unique file name.
   
7. Tell the server to run the executable.

        > 40
        8

  Upon completion, the server responds with `ACK (8)`.
   
8. Obtain stderr.

        > 50 255
        59 ...

  The server responds with message `59` containing `stderr`.
       
9. Obtain stdout.

        > 50 254
        59 ...

  The server responds with message `59` containing `stdout`.
  
10. Obtain first output file (numbered `0`)

        > 50 0
        59 ...

  The server responds with message `59` containing the output.
       
11.  Obtain second output file (numbered `1`)

        > 50 1
        9

  Since we did not specify a second output file parameter, the server responds with `NACK (9)`.
  
12. Close the connection.

        > x
        
  The server will remove all generated files.
