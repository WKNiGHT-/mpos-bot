import urllib
import logging
import json

def ticker_run_cmd(line, config):
    logger = logging.getLogger('bot.cmd.ticker')
    url = urllib.urlopen('https://btc-e.com/api/2/ltc_usd/ticker')
    if url.getcode() != 200:
        logger.error('Request failed with http error: ' + str(url.getcode()))
        return False
    data_parse = json.loads(url.read())
    logger.info('Completed command')
    return 'PRIVMSG ' + config['channel'] + ' :' + '[BTC-E/ticker] > Last: ' + str(data_parse['ticker']['last']) + ' | High: ' + str(data_parse['ticker']['high']) + ' | Low: ' + str(data_parse['ticker']['low']) + ' | Avg: ' + str(data_parse['ticker']['avg'])
