import urllib
import logging
import json

def fortune_run_cmd(line, config):
    logger = logging.getLogger()
    url = urllib.urlopen('http://www.iheartquotes.com/api/v1/random')
    fortune = url.read()
    return 'PRIVMSG ' + config['channel'] + ' :' + fortune
