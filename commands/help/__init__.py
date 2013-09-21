import urllib
import logging
import json

def run(line, config):
    logger = logging.getLogger()
    return 'PRIVMSG ' + config['channel'] + ' :Commands supported: !status, !u, !last'
