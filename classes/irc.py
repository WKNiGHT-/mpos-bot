import socket
import logging
import string
import select

class IRC:
    def __init__(self):
        self.logger = logging.getLogger()
        self.readbuffer= ""
        self.data = {}
    def connect(self, host, port):
        self.logger.info('Connecting to IRC host: ' + host)
        self.socket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        self.socket.connect((host, port ))
        self.socket.setblocking(0)
    def join(self, channel):
        self.send('JOIN ' + channel)
    def nick(self, nick):
        self.send('NICK ' + nick)
    def user(self, user):
        self.send('USER ' + user)
    def pong(self, line):
        self.send('PONG ' + line.split()[1])
    def send(self, message):
        self.logger.debug('irc.send:' + message)
        self.socket.send(message + '\n')
    def check(self, timeout=0):
        ready = select.select([self.socket], [], [], timeout)
        if ready[0]:
            return True
        return False
    def recv(self, size):
        self.readbuffer = self.readbuffer + self.socket.recv(size)
        self.data = string.split(self.readbuffer, "\n")
        self.readbuffer = self.data.pop()
        return self.data
