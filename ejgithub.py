#!/usr/bin/python -B
import os, sys, ConfigParser, logging, signal, string, time

sys.path.insert(1, './classes')
sys.path.insert(1, './lib')
from irc import *
from blockupdate import *
from commands import *
import settings

# Load our local configuration
config = ConfigParser.RawConfigParser()
if not config.read('conf/config.cfg'):
    raise RuntimeError('Failed to load configuration: conf/config.cfg')
settings = settings.load(config)

# Setup logging according to configuration
numeric_level = getattr(logging, config.get('Logging', 'level').upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % config.get('Logging', 'level'))
logging.basicConfig(format=config.get('Logging', 'format'), level=numeric_level)

# Create IRC Object and runn connect
irc = IRC()
irc.connect(settings['host'], settings['port'])
irc.nick(settings['nick'])
irc.user(settings['user'])
irc.join(settings['channel'])

# Load our commands
commands = Commands()
commands.setConfig(settings)

# Load the blockupdate checker class
blockupdate = BlockUpdate()
blockupdate.setConfig(settings)

# What to do on a reload request
def reload_bot(signum, stack):
    commands.rehash()

# Call our reload function when receiving SIGUSR1
signal.signal(signal.SIGUSR1, reload_bot)

while True:
    # Holds our lines returned from socket
    data = {}

    # Check for a new block before checking IRC
    try:
        if blockupdate.check():
            irc.send(blockupdate.getMessage())
    except Exception as exception:
        logging.exception('Failed to run blockupdate:')

    try:
        if irc.check():
            data = irc.recv(256)
    except Exception as exception:
        logging.exception('Failed to read from socket:')

    for line in data:
        # Remove '\r' from line
        line = string.rstrip(line)
        logging.debug(line)

        if line.find ( 'PING' ) != -1:
            irc.pong(line)
        elif commands.check(line):
            try:
                irc.send(commands.run())
            except Exception as exception:
                logging.exception('Command execution failed:')
    time.sleep(1)
