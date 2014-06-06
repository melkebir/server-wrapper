#!/usr/bin/python
import multiprocessing
import socket
from messages import ClientMessage
from messages import ServerMessage
import messages
import os

def handleRegularParameter(m, parameters):
    assert m.message_type == messages.CLIENT_MESSAGE_REGULAR_PARAMETER
    parameters += [str(m.name), str(m.payload)]

def handleInputFileParameter(m, address, tmp_dir, parameters):
    assert m.message_type == messages.CLIENT_MESSAGE_INPUT_FILE_PARAMETER
    filename = tmp_dir + "/" + str(address[0]) + "_" + str(address[1]) + "_" + str(len(parameters) / 2) + ".in"
    with open(filename, 'wb') as output:
        output.write(m.payload)

    parameters += [str(m.name), filename]

def handleOutputFileParameter(m, address, tmp_dir, parameters):
    assert m.message_type == messages.CLIENT_MESSAGE_OUTPUT_FILE_PARAMETER
    filename = tmp_dir + "/" + str(address[0]) + "_" + str(address[1]) + "_" + str(len(parameters) / 2) + ".out"
    parameters += [str(m.name), filename]

def handleRunRequest(executable, parameters, inputFileParameters, outputFileParameters):
    from subprocess import Popen, PIPE
    process = Popen(executable.split(" ") + parameters + inputFileParameters + outputFileParameters, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr

def handle(S, executable, tmp_dir, connection, address):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    parameters = []
    inputFileParameters = []
    outputFileParameters = []
    stdout = None
    stderr = None
    
    try:
        logger.debug("Connected %r at %r", connection, address)

        while True:
            m = ClientMessage.receive(connection)
            if m.message_type == messages.CLIENT_MESSAGE_ALIVE:
                ServerMessage(messages.SERVER_MESSAGE_ACK).send(connection)
            elif m.message_type == messages.CLIENT_MESSAGE_REGULAR_PARAMETER:
                if m.name_length == 0:
                    ServerMessage(messages.SERVER_MESSAGE_NACK).send(connection)
                else:
                    handleRegularParameter(m, parameters)
                    ServerMessage(messages.SERVER_MESSAGE_ACK).send(connection)
            elif m.message_type == messages.CLIENT_MESSAGE_INPUT_FILE_PARAMETER:
                handleInputFileParameter(m, address, tmp_dir, inputFileParameters)
                ServerMessage(messages.SERVER_MESSAGE_ACK).send(connection)
            elif m.message_type == messages.CLIENT_MESSAGE_OUTPUT_FILE_PARAMETER:
                handleOutputFileParameter(m, address, tmp_dir, outputFileParameters)
                ServerMessage(messages.SERVER_MESSAGE_ACK).send(connection)
            elif m.message_type == messages.CLIENT_MESSAGE_RUN:
                S.acquire()
                logger.debug("Executing %s", executable)
                stdout, stderr = handleRunRequest(executable, parameters, inputFileParameters, outputFileParameters)
                S.release()
                ServerMessage(messages.SERVER_MESSAGE_ACK).send(connection)
            elif m.message_type == messages.CLIENT_MESSAGE_GET_OUTPUT:
                # 255 = stderr
                # 254 = stdout
                try:
                    i = int(m.name)
                    if i == 255:
                        if stderr == None or len(stderr) == 0:
                            ServerMessage(messages.SERVER_MESSAGE_OUTPUT, 0).send(connection)
                        else:
                            ServerMessage(messages.SERVER_MESSAGE_OUTPUT, len(stderr), stderr).send(connection)
                    elif i == 254:
                        if stdout == None or len(stdout) == 0:
                            ServerMessage(messages.SERVER_MESSAGE_OUTPUT, 0).send(connection)
                        else:
                            ServerMessage(messages.SERVER_MESSAGE_OUTPUT, len(stdout), stdout).send(connection)
                    elif 0 <= i and i < len(outputFileParameters) / 2:
                        with open(outputFileParameters[2*i + 1], "rb") as f:
                            payload =  bytearray(f.read())
                            ServerMessage(messages.SERVER_MESSAGE_OUTPUT, len(payload), payload).send(connection)
                    else:
                        ServerMessage(messages.SERVER_MESSAGE_NACK).send(connection)
                except:
                    ServerMessage(messages.SERVER_MESSAGE_NACK).send(connection)
            else:
                ServerMessage(messages.SERVER_MESSAGE_NACK).send(connection)

            #logger.debug("Received message %d %s %s", m.message_type, m.name, m.payload)
            logger.debug("Received message %d", m.message_type)
    except IOError:
        logger.debug("Connection dropped")
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")

        # cleanup the mess...
        for i in range(len(inputFileParameters) / 2):
            logger.debug("Removing %s", inputFileParameters[2*i + 1])
            os.remove(inputFileParameters[2*i + 1])
        for i in range(len(outputFileParameters) / 2):
            logger.debug("Removing %s", outputFileParameters[2*i + 1])
            if os.path.exists(outputFileParameters[2*i + 1]):
                os.remove(outputFileParameters[2*i + 1])

        logger.debug(" ".join(parameters + inputFileParameters + outputFileParameters))
        connection.close()
 
class Server(object):
    def __init__(self, hostname, port, queue_size, executable, tmp_dir):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port
        self.queue_size = queue_size
        self.executable = executable
        self.tmp_dir = tmp_dir
 
    def start(self):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        S = multiprocessing.BoundedSemaphore(queue_size)
 
        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(S, self.executable, self.tmp_dir, conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

def usage(out):
    import sys
    sys.stderr.write("Usage: " + sys.argv[0] + " <PORT_NUMBER> <QUEUE_SIZE> <TMP_DIR> <EXECUTABLE>\n")
 
if __name__ == "__main__":
    import logging
    import sys

    if (len(sys.argv) != 5):
        usage(sys.stderr)
        sys.exit(1)
    else:
        try:
            port_number = int(sys.argv[1])
            queue_size = int(sys.argv[2])
            tmp_dir = sys.argv[3]
            executable = sys.argv[4]
        except ValueError as e:
            print "ValueError error: {0}".format(e)
            usage(sys.stderr)
            sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", port_number, queue_size, executable, tmp_dir)
    try:
        logging.info("Listening")
        server.start()
    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
    logging.info("All done")
