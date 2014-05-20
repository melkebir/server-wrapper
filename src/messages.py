import socket

class ClientMessage(object):
    def __init__(self, message_type, name_length, name, payload_length, payload):
        self.message_type = message_type
	self.name_length = name_length
	self.name = name
	self.payload_length = payload_length
	self.payload = payload

    @classmethod
    def receive_bytes(cls, connection, size):
        b = bytearray(connection.recv(size))
	if b:
	    return b
	else:
	    raise IOError("Connection dropped")

    @classmethod
    def receive(cls, connection):
        import struct

        message_type = cls.receive_bytes(connection, 1)[0]

	name_length = struct.unpack("!i", cls.receive_bytes(connection, 4))[0]
	name = cls.receive_bytes(connection, name_length)

        assert len(name) == name_length

	payload_length = struct.unpack("!i", connection.recv(4))[0]
	payload = cls.receive_bytes(connection, payload_length)

	assert len(payload) == payload_length

        return cls(message_type, name_length, name, payload_length, payload)

    def send(self, connection):
        import struct
        connection.send(bytearray([self.message_type]))
	connection.send(bytearray(struct.pack("!i", self.name_length)))
	connection.send(bytearray(self.name))
	connection.send(bytearray(struct.pack("!i", self.payload_length)))
	connection.send(bytearray(self.payload))