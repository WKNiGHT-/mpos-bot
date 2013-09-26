import socket
import json
import urllib
import logging
import datetime

class BlockUpdate:
    def __init__(self):
        self.last_fast_check = datetime.datetime.now()
        self.logger = logging.getLogger('bot.blockupdate')
        self.logger.info('Initilized blockupdater')
        self.prevblock_height = 0
        self.message = ''
        self.errorcount = 0
        self.enabled = True
    def setConfig(self, config):
        self.config = config
    def getMessage(self):
        return self.message
    def check(self):
        if not self.enabled:
            return False
        if self.last_fast_check < (datetime.datetime.now() - datetime.timedelta(seconds=self.config['interval'])):
            self.logger.debug('Checking for new block')
            self.last_fast_check = datetime.datetime.now()
            url = urllib.urlopen(self.config['api_url'] + '&action=getblocksfound&api_key=' + self.config['api_key'] + '&limit=1')
            if url.getcode() != 200:
                self.logger.error('Blockupdate failed, URL returned http error: ' + str(url.getcode()))
                self.errorcount += 1
                if self.errorcount == 5:
                    self.logger.warning('Disabled blockupdate due to frequent errors')
                    self.enabled = False
            else:
                self.errorcount = 0
                block = json.loads(url.read())
                block_height = str(block['getblocksfound']['data'][0]['height'])
                block_height = int(block['getblocksfound']['data'][0]['height'])
                if self.prevblock_height == 0:
                    self.prevblock_height = block_height
                elif self.prevblock_height != block_height:
                    self.prevblock_height = block_height
                    self.message = 'PRIVMSG ' + self.config['channel'] + '' +u' :BLOCK FOUND: ' + str(block['getblocksfound']['data'][0]['height']) + ' | ' + str(block['getblocksfound']['data'][0]['shares']) + ' shares | Amount: ' + str(block['getblocksfound']['data'][0]['amount']) + ' | Found By ' + str(block['getblocksfound']['data'][0]['finder'])
                    return True
            return False
