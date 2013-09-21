import urllib
import logging
import json

def norris_run_cmd(line, config):
    logger = logging.getLogger()
    url = urllib.urlopen('http://api.icndb.com/jokes/random')
    joke = json.loads(url.read())
    return 'PRIVMSG ' + config['channel'] + ' :' + joke['value']['joke']
