Server-wrapper
==============

Protocol
--------

A message is structured as follows.

     _______________________________________________________
    |       |             |      |                |         |
    | type  | name_length | name | payload_length | payload |
    | (int) | (int)       |      | (int)          |         |
    |_______|_____________|______|________________|_________|

There are 5 message `types`:

1. Regular parameter
2. Input file parameter
3. Output file parameter
4. Run
5. Query whether finished
6. Not finished response
7. Finished response
8. Fetch result request
9. Result

