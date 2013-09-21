import socket
import json
import urllib
import logging
import datetime

class BlockUpdate:
    def __init__(self):
        self.last_fast_check = datetime.datetime.now()
        self.logger = logging.getLogger()
        self.prevblock_height = 0
        self.message = ''

    def setConfig(self, config):
        self.config = config

    def getMessage(self):
        return self.message

    def check(self):
        if self.last_fast_check < (datetime.datetime.now() - datetime.timedelta(seconds=self.config['interval'])):
            self.logger.debug('Checking for new block')
            self.last_fast_check = datetime.datetime.now()
            url = urllib.urlopen(self.config['api_url'] + '&action=getblocksfound&api_key=' + self.config['api_key'] + '&limit=1')
            block = json.loads(url.read())
            block_height = str(block['getblocksfound']['data'][0]['height'])
            try:
                block_height = int(block['getblocksfound']['data'][0]['height'])
                if self.prevblock_height == 0:
                    self.prevblock_height = block_height
                elif self.prevblock_height != block_height:
                    self.prevblock_height = block_height
                    self.message = 'PRIVMSG ' + self.config['channel'] + '' +u' :BLOCK FOUND: ' + str(block['getblocksfound']['data'][0]['height']) + ' | ' + str(block['getblocksfound']['data'][0]['shares']) + ' shares | Amount: ' + str(block['getblocksfound']['data'][0]['amount']) + ' | Found By ' + str(block['getblocksfound']['data'][0]['finder'])
                    return True
            except IOError, e:
                self.message = 'PRIVMSG ' + self.config['channel'] + '\x02\x034ERROR:  \x02\x030|\x034 Pool \x030|\x034 DOWN'
            except socket.error, e:
                self.message = 'PRIVMSG ' + self.config['channel'] + '\x02\x034ERROR:  \x02\x030|\x034 Pool \x030|\x034 DOWN'
            else:
                self.message = 'PRIVMSG ' + self.config['channel'] + '\x02\x033ONLINE: \x02\x030|\x033 Pool \x030|\x034 UP'
        return False
