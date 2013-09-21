import imp
import logging
import os

MainModule = "__init__"

class Commands:
    def __init__(self):
        self.logger = logging.getLogger()
        self.folder = './commands'
        self.commands = self.getCommands()
        self.command_to_run = ''
        self.line = ''

    def setConfig(self, config):
        self.config = config

    def getCommands(self):
        self.logger.debug('Trying to find commands in ' + self.folder)
        plugins = []
        possibleplugins = os.listdir(self.folder)
        for i in possibleplugins:
            location = os.path.join(self.folder, i)
            if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
                continue
            info = imp.find_module(MainModule, [location])
            self.logger.debug('Found command: ' + i)
            plugins.append({"name": i, "info": info})
        return plugins

    def rehash(self, signum, stack):
        self.logger.info('Rehash requested')
        self.commands = self.getCommands()
        return True

    def check(self, line):
        """ Check if we have a command request """
        if line.find(':!') != -1:
            self.line = line
            strCommand = line.split(':!')[1].split(' ')[0]
            self.logger.debug('Found a command string: ' + strCommand)
            for command in self.commands:
                if command['name'] == strCommand:
                    self.logger.debug('Found matching command: ' + command['name'])
                    self.command_to_run = command
                    return True
        return False

    def run(self):
        self.logger.debug(str(self.command_to_run))
        module = imp.load_module(MainModule, *self.command_to_run["info"])
        methodToCall = getattr(module, self.command_to_run['name'] + '_run_cmd')
        return methodToCall(self.line, self.config)
