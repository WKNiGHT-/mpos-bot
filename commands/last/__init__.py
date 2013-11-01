import urllib
import logging
import json

def last_run_cmd(line, config):
    logger = logging.getLogger('bot.cmd.last')
    logger.debug('Running command cmd.last')
    url = urllib.urlopen(config['api_url'] + '&action=getblocksfound&api_key=' + config['api_key'] + '&limit=1')
    if url.getcode() != 200:
        logger.error('Request failed with http error: ' + str(url.getcode()))
        return False
    jsonData = json.loads(url.read())
    logger.info('Completed command')
    return 'PRIVMSG ' + config['channel'] + ' :' + 'Last Block: #' + str(jsonData['getblocksfound']['data'][0]['height']) + ' | Shares: ' + str(jsonData['getblocksfound']['data'][0]['shares']) + ' | Confirmations: ' + str(jsonData['getblocksfound']['data'][0]['confirmations']) + ' | Solved By: ' + str(jsonData['getblocksfound']['data'][0]['finder'])
