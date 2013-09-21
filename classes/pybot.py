from daemon import *

class PyBot(Daemon):
    def run(self):
        self.logger = logging.getLogger()
        self.irc = irc.getIrc()
        while True:
            try:
                line = irc.recv(512)
            except:
                logging.debug('Skipped recv')
            logging.debug(line)
            if line.find ( 'PING' ) != -1:
                self.irc.send( 'PONG ' + line.split() [ 1 ] )
            elif commands.check(line):
                try:
                    self.irc.send(commands.run())
                except:
                    logging.debug('Failed to run command')
                if blockupdate.check():
                    self.irc.send(blockupdate.getMessage())
