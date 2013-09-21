import urllib
import logging
import json

def help_run_cmd(line, config):
    logger = logging.getLogger()
    return 'PRIVMSG ' + config['channel'] + ' :Commands supported: !status, !u, !last, !norris, !fortune'
