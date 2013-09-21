import urllib
import logging
import json

def run(line, config):
    logger = logging.getLogger()
    url = urllib.urlopen('https://btc-e.com/api/2/ltc_usd/ticker')
    data_parse = json.loads(url.read())
    return 'PRIVMSG ' + config['channel'] + ' :' + '[BTC-E/ticker] > Last: ' + str(data_parse['ticker']['last']) + ' | High: ' + str(data_parse['ticker']['high']) + ' | Low: ' + str(data_parse['ticker']['low']) + ' | Avg: ' + str(data_parse['ticker']['avg'])
