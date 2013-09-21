import urllib
import logging
import json

def status_run_cmd(line, config):
    logger = logging.getLogger()
    url = urllib.urlopen(config['api_url'] + '&action=public')
    status = json.loads(url.read())
    return 'PRIVMSG ' + config['channel'] + ' :' + str(status['pool_name']) + ' Last Block: ' + str(status['last_block']) + ' | Shares This Round: ' + str(status['shares_this_round']) + ' | Current Hashrate: ' + str(status['hashrate']) + ' kh/s' +  ' | Currently '+ str(status['workers']) + ' workers'
