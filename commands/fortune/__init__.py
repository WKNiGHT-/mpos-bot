import urllib
import logging
import json

def fortune_run_cmd(line, config):
    logger = logging.getLogger('bot.cmd.fortune')
    data = urllib.urlopen('http://www.iheartquotes.com/api/v1/random').read(20000)
    data = data.split('\n')
    fortune= ''
    for line in data:
        fortune = fortune+' '+line
    return 'PRIVMSG ' + config['channel'] + ' :' + fortune
