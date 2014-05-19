#!/usr/bin/python
import multiprocessing
import socket
 
def handle(connection, address):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)
            connection.sendall(data)
            logger.debug("Sent data")
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
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
 
        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)

def usage(out):
    import sys
    sys.stderr.write("Usage: " + sys.argv[0] + " <QUEUE_SIZE> <TMP_DIR> <EXECUTABLE>\n")
 
if __name__ == "__main__":
    import logging
    import sys

    if (len(sys.argv) != 4):
        usage(sys.stderr)
        sys.exit(1)
    else:
        try:
            queue_size = int(sys.argv[1])
            tmp_dir = sys.argv[2]
            executable = sys.argv[3]
        except ValueError as e:
            print "ValueError error: {0}".format(e)
            usage(sys.stderr)
            sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", 9000, queue_size, executable, tmp_dir)
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