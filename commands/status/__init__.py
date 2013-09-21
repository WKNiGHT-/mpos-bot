import urllib
import logging
import json
import locale

def status_run_cmd(line, config):
    locale.setlocale(locale.LC_ALL, 'en_US')
    logger = logging.getLogger()
    url = urllib.urlopen(config['api_url'] + '&action=getpoolstatus&api_key=' + config['api_key'])
    jsonData = json.loads(urllib.urlopen(config['api_url'] + '&action=getpoolstatus&api_key=' + config['api_key']).read())
    jsonPublicData = json.loads(urllib.urlopen(config['api_url'] + '&action=public').read())
    strEfficiency = str(jsonData['getpoolstatus']['data']['efficiency']) + '%'
    strDifficulty = str(round(jsonData['getpoolstatus']['data']['networkdiff'], 3))
    strRoundEstimate = str(locale.format('%d', round(jsonData['getpoolstatus']['data']['estshares'], 0), grouping=True))
    strCurrentRound = str(locale.format('%d', round(jsonPublicData['shares_this_round'], 0), grouping=True))
    strHashrate = str(locale.format('%d', round(jsonPublicData['hashrate'], 2), grouping=True))
    strPoolLuck = str(round(jsonPublicData['shares_this_round'] / jsonData['getpoolstatus']['data']['estshares'] * 100, 2))
    strWorkers = str(jsonPublicData['workers'])
    return 'PRIVMSG ' + config['channel'] + ' :Pool Hashrate: ' + strHashrate + ' khash | Pool Efficiency: ' + strEfficiency + ' | Current difficulty: ' + strDifficulty + ' | Round Estimate: ' + strRoundEstimate + ' | Current Round: ' + strCurrentRound + ' | Pool Luck: ' + strPoolLuck + '% | Workers: ' + strWorkers
