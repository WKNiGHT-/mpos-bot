import urllib
import logging
import json

def norris_run_cmd(line, config):
    logger = logging.getLogger('bot.cmd.norris')
    url = urllib.urlopen('http://api.icndb.com/jokes/random')
    joke = json.loads(url.read())
    logger.info('Completed command')
    return 'PRIVMSG ' + config['channel'] + ' :' + joke['value']['joke']
