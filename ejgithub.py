#!/usr/bin/python -B
import os
import sys
import ConfigParser
import logging

sys.path.insert(1, './classes')
from irc import *
from blockupdate import *
from commands import *

config = ConfigParser.RawConfigParser()
if not config.read('conf/config.cfg'):
    raise RuntimeError('Failed to load configuration: conf/config.cfg')

# Convert to numeric loglevel
numeric_level = getattr(logging, config.get('Logging', 'level').upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % config.get('Logging', 'level'))
logging.basicConfig(format=config.get('Logging', 'format'), level=numeric_level)

# Convert our config file
settings = {}
settings['host'] = config.get('IRC', 'host')
settings['port'] = config.getint('IRC', 'port')
settings['nick'] = config.get('IRC', 'nick')
settings['user'] = config.get('IRC', 'user')
settings['channel'] = config.get('IRC', 'channel')
settings['interval'] = config.getint('Blockupdate', 'interval')
settings['api_key'] = config.get('API', 'key')
settings['api_url'] = config.get('API', 'url')

irc = IRC()
irc.connect(settings['host'], settings['port'])
irc.send( 'NICK ' + settings['nick'] )
irc.send( 'USER ' + settings['user'])
irc.send( 'JOIN ' + settings['channel'])

# Load our commands
commands = Commands()
commands.setConfig(settings)

# Load the blockupdate checker class
blockupdate = BlockUpdate()
blockupdate.setConfig(settings)

while True:
    line = irc.recv(4096)
    logging.debug(line)

    if line.find ( 'PING' ) != -1:
        irc.send( 'PONG ' + line.split() [ 1 ] )
    elif commands.check(line):
        irc.send(commands.run())

    if blockupdate.check():
        irc.send(blockupdate.getMessage())
