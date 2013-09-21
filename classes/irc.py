import socket
import logging

class IRC:
    def __init__(self):
        self.logger = logging.getLogger()
    def connect(self, host, port):
        self.logger.info("Connecting to IRC host: " + host)
        self.irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.irc.connect((host, port ))
    def send(self, message):
        self.logger.debug(message)
        self.irc.send(message + '\n')
    def recv(self, size):
        return self.irc.recv(size).strip()
