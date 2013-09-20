import socket
import json
import urllib
import datetime
import logging

errorcode_ltc = 0
bitcoindID_ltc = "0"
prevblock_height = 0
dbmult = 1

##################
#                #
#  Logging       #
#                #
##################
FORMAT="%(asctime)s  :  %(message)s"

###################
#                 #
#  API Settings   #
#                 #
###################
sURL = 'YOUR_API_URL'
API_KEY = "YOUR_ADMIN_API_KEY"

###################
#                 #
#   IRC Settings  #
#                 #
###################
sChannel = '#your-channel'
sNetwork = 'hitchcock.freenode.net'
iPort = 6667
sNick = 'YourBotNick'
sUser = 'anon anon anon :EJGithub'

#############################################################
#############################################################
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

# Wrapper function to log and send to IRC
def sendIrc(data):
    logger = logging.getLogger()
    logger.debug(data)
    irc.send(data)

logging.info("Connecting to IRC network: " + sNetwork)
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( sNetwork, iPort ) )
# logging.debug(irc.recv ( 1024))
logging.debug("Setting nickname: " + sNick)
sendIrc ( 'NICK ' + sNick + '\n' )
logging.debug("Setting user: " + sUser)
sendIrc ( 'USER ' + sUser + '\n' )
logging.debug("Joining channel: " + sChannel)
sendIrc ( 'JOIN ' + sChannel + '\n' )
last_fast_check = datetime.datetime.now()

while True:
    data = irc.recv ( 4096 )
    logging.debug(data)
    if data.find ( 'PING' ) != -1:
        sendIrc ( 'PONG ' + data.split() [ 1 ] + '\n' )

    if data.find(sChannel + ' :!help') != -1:
        sendIrc ( 'PRIVMSG ' + sChannel + ' : ' + sChannel + ' Bot Commands. !status !last !ticker !u !donations \n')

    if data.find(sChannel + ' :!donations') != -1:
        sendIrc ( 'PRIVMSG ' + sChannel + ' : Pool Donations change_this_to_your_ltc_address | Bot Donations goes to WKNiGHT at LewixZv4FMuz5dzxUqrH9P1SR2DvaxTmef \n')

    if data.find(sChannel + ' :!status') != -1:
            url = urllib.urlopen(sURL + '&action=public')
            status = url.read()
            status = json.loads(status)
            sendIrc ( 'PRIVMSG ' + sChannel + ' :' + str(status['pool_name']) + ' Last Block: ' + str(status['last_block']) + ' | Shares This Round: ' + str(status['shares_this_round']) + ' | Current Hashrate: ' + str(status['hashrate']) + ' kh/s' +  ' | Currently '+ str(status['workers']) + ' workers' '\n')

    if data.find(sChannel + ' :!last') != -1:
        url = urllib.urlopen(sURL + '&action=getblocksfound&api_key=' + API_KEY + '&limit=1')
        status = url.read()
        status = json.loads(status)
        sendIrc ( 'PRIVMSG ' + sChannel + ' :' + 'Last Block: #' + str(status['getblocksfound']['data'][0]['height']) + ' | Shares: ' + str(status['getblocksfound']['data'][0]['shares']) + ' | Confirmations: ' + str(status['getblocksfound']['data'][0]['confirmations']) + ' | Solved By: ' + str(status['getblocksfound']['data'][0]['finder']) + '\n')

    if data.find(sChannel + ' :!ticker') != -1:
        url = urllib.urlopen('https://www.btc-e.com/api/2/10/ticker')
        data_parse = url.read()
        data_parse = json.loads(data_parse)
        sendIrc ( 'PRIVMSG ' + sChannel + ' :' + '[BTC-E/ticker] > Last: ' + str(data_parse['ticker']['last']) + ' | High: ' + str(data_parse['ticker']['high']) + ' | Low: ' + str(data_parse['ticker']['low']) + ' | Avg: ' + str(data_parse['ticker']['avg']) + '\n') 

    if data.find(sChannel + ' :!u') != -1:
        userCommand = data.split(':')[2]
        userNick = userCommand.split(' ')

        if len(userNick) == 2:
            userNick = userNick[1]
            url = urllib.urlopen(sURL + '&action=getuserstatus&api_key=' + API_KEY + '&id=' + userNick)
            data_parse = url.read()
            data_parse = json.loads(data_parse)
            sendIrc ( 'PRIVMSG ' + sChannel + ' :' + 'Username: ' + str(data_parse['getuserstatus']['data']['username']) + ' | Hashrate: ' + str(data_parse['getuserstatus']['data']['hashrate']) + ' kh/s' + ' | Shares Valid: ' + str(data_parse['getuserstatus']['data']['shares']['valid']) + ' | Shares Invalid: ' + str(data_parse['getuserstatus']['data']['shares']['invalid']) + '\n')


        else:
            print 'no user specified'
            sendIrc ( 'PRIVMSG ' + sChannel + ' :' + 'User not known' + '\n')

    now = datetime.datetime.now()
    if last_fast_check < (now - datetime.timedelta(seconds=20*dbmult)):
        logging.debug('Checking Pool for new blocks')
        last_block_check = datetime.datetime.now()
        url = urllib.urlopen(sURL + '&action=getblocksfound&api_key=' + API_KEY + '&limit=1')
        block = url.read()
        block = json.loads(block)
        block_height = str(block['getblocksfound']['data'][0]['height'])
        try:
            block_height = int(block['getblocksfound']['data'][0]['height'])
            if prevblock_height == 0:
                prevblock_height = block_height
            elif prevblock_height != block_height:

                sendIrc('PRIVMSG ' + sChannel + '' +u' :BLOCK FOUND: ' + str(block['getblocksfound']['data'][0]['height']) + ' | ' + str(block['getblocksfound']['data'][0]['shares']) + ' shares | Amount: ' + str(block['getblocksfound']['data'][0]['amount']) + ' | Found By ' + str(block['getblocksfound']['data'][0]['finder']) + '\n') 
                prevblock_height = block_height
        except IOError, e:
            print e[0], e[1]
            errorcode_ltc = 1
            sendIrc('#' + sChannel + '','\x02\x034ERROR:  \x02\x030|\x034 Pool \x030|\x034 DOWN')
        except socket.error, e:
            print e
            errorcode_ltc = 1
            sendIrc('#' + sChannel + '','\x02\x034ERROR:  \x02\x030|\x034 Pool \x030|\x034 DOWN')
        else:
            if errorcode_ltc == 1:
                sendIrc('#' + sChannel + '','\x02\x033ONLINE: \x02\x030|\x033 Pool \x030|\x034 UP')
                errorcode_ltc = 0 
