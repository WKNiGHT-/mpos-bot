#!/usr/bin/python -B
import os, sys, ConfigParser, logging, signal, string, time
from daemon import runner

working_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, working_directory + '/classes')
sys.path.insert(1, working_directory + '/lib')
import settings
from irc import *
from blockupdate import *
from commands import *

# Load our local configuration
config = ConfigParser.RawConfigParser()
if not config.read(working_directory + '/conf/config.cfg'):
    raise RuntimeError('Failed to load configuration: conf/config.cfg')
settings = settings.load(config)

# Ensure some paths exist
logfile = working_directory + '/' + config.get('Logging', 'file')
if not os.path.exists(os.path.dirname(logfile)):
    os.makedirs(os.path.dirname(logfile))

# Setup logging according to configuration
numeric_level = getattr(logging, config.get('Logging', 'level').upper(), None)
formatter = config.get('Logging', 'format')
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % config.get('Logging', 'level'))
logging.basicConfig(format=formatter, level=numeric_level)
logFormatter = logging.Formatter(formatter)
logger = logging.getLogger('bot')
fh = logging.FileHandler(logfile)
fh.setFormatter(logFormatter)
logger.addHandler(fh)
logger.info('Starting IRC bot')

def reload_program_config(signum, stack):
    logger.info('Reloading bot configuration')
    commands.rehash()

def main():
    global commands
    logger = logging.getLogger('bot.worker')
    logger.info('Entering bot worker process')

    # Call our reload function when receiving SIGUSR1
    # signal.signal(signal.SIGUSR1, reload_bot)
    logger.debug('Trying to fetch available commands')

    # Load our commands from working directory
    commands = Commands(working_directory)
    commands.setConfig(settings)

    # Load the blockupdate checker class
    blockupdate = BlockUpdate()
    blockupdate.setConfig(settings)

    # Create IRC Object and run connect
    irc = IRC()
    irc.connect(settings['host'], settings['port'])
    irc.nick(settings['nick'])
    irc.user(settings['user'])
    irc.join(settings['channel'])

    logger.info('Entering process loop')
    while True:
        # Holds our lines returned from socket
        data = {}

        # Check for a new block before checking IRC
        try:
            if blockupdate.check():
                irc.send(blockupdate.getMessage())
                logger.info('Blockupdate completed')
        except Exception as exception:
            logger.exception('Failed to run blockupdate:')

        try:
            if irc.check():
                data = irc.recv(4096)
        except Exception as exception:
            logger.exception('Failed to read from socket:')

        for line in data:
            # Remove '\r' from line
            line = string.rstrip(line)
            logger.debug(line)

            if line.find ( 'PING' ) != -1:
                irc.pong(line)
            elif commands.check(line):
                try:
                    data = commands.run()
                    if data:
                        irc.send(data)
                except Exception as exception:
                    logger.exception('Command execution failed:')
        time.sleep(0.5)


class App():
    """
        Daemon runner application class
    """
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path =  working_directory + '/bot.pid'
        self.pidfile_timeout = 5

    def run(self):
        logger.debug('Created daemon context')
        try:
            main()
        except:
            logger.debug('Failed to execute main run loop')


if __name__ == '__main__':
    app = App()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.daemon_context.working_directory = working_directory
    daemon_runner.daemon_context.files_preserve = [fh.stream]
    daemon_runner.daemon_context.signal_map = {
        signal.SIGUSR1: reload_program_config
    }
    daemon_runner.do_action()
