import urllib
import logging
import json

def help_run_cmd(line, config):
    logger = logging.getLogger('bot.cmd.help')
    return 'PRIVMSG ' + config['channel'] + ' :Commands supported: !status, !u, !last, !norris, !fortune'
