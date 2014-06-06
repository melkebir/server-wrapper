import socket

SERVER_MESSAGE_ACK = 8
SERVER_MESSAGE_NACK = 9
SERVER_MESSAGE_OUTPUT = 59

CLIENT_MESSAGE_ALIVE = 0
CLIENT_MESSAGE_REGULAR_PARAMETER = 10
CLIENT_MESSAGE_INPUT_FILE_PARAMETER = 20
CLIENT_MESSAGE_OUTPUT_FILE_PARAMETER = 30
CLIENT_MESSAGE_RUN = 40
CLIENT_MESSAGE_GET_OUTPUT = 50

class ServerMessage(object):
    def __init__(self, message_type, payload_length = 0, payload = ""):
        self.message_type = message_type
        self.payload_length = payload_length
        self.payload = payload

    @classmethod
    def receive_bytes(cls, connection, size):
        if size == 0:
            b = bytearray()
        else:
            b = bytearray(connection.recv(size))
        if len(b) != size:
            raise IOError("Connection dropped")
        return b

    @classmethod
    def receive(cls, connection):
        import struct

        message_type = cls.receive_bytes(connection, 1)[0]

        payload_length_bytes = cls.receive_bytes(connection, 4)
        # unpack the network-byte-order bytes into an int
        payload_length = struct.unpack("!i", str(payload_length_bytes))[0]
        payload = cls.receive_bytes(connection, payload_length)

        return cls(message_type, payload_length, payload)

    def send(self, connection):
        import struct
        connection.send(bytearray([self.message_type]))
        connection.send(bytearray(struct.pack("!i", self.payload_length)))
        if self.payload_length != 0:
            connection.send(bytearray(self.payload))

class ClientMessage(object):
    def __init__(self, message_type, name_length, name, payload_length, payload):
        self.message_type = message_type
        self.name_length = name_length
        self.name = name
        self.payload_length = payload_length
        self.payload = payload

    @classmethod
    def receive_bytes(cls, connection, size):
        if size == 0:
            b = bytearray()
        else:
            b = bytearray(connection.recv(size))
        if len(b) != size:
            raise IOError("Connection dropped")
        return b

    @classmethod
    def receive(cls, connection):
        import struct

        message_type = cls.receive_bytes(connection, 1)[0]

        name_length_bytes = cls.receive_bytes(connection, 4)
        # unpack the network-byte-order bytes into an int
        name_length = struct.unpack("!i", str(name_length_bytes))[0]
        name = cls.receive_bytes(connection, name_length)

        payload_length_bytes = cls.receive_bytes(connection, 4)
        # unpack the network-byte-order bytes into an int
        payload_length = struct.unpack("!i", str(payload_length_bytes))[0]
        payload = cls.receive_bytes(connection, payload_length)

        return cls(message_type, name_length, name, payload_length, payload)

    def send(self, connection):
        import struct
        connection.send(bytearray([self.message_type]))
        connection.send(bytearray(struct.pack("!i", self.name_length)))
        connection.send(bytearray(self.name))
        connection.send(bytearray(struct.pack("!i", self.payload_length)))
        connection.send(bytearray(self.payload))
