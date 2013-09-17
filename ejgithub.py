import socket
import json
import urllib
import datetime
errorcode_ltc = 0
bitcoindID_ltc = "0"
prevblock_height = 0
dbmult = 1
 
network = 'hitchcock.freenode.net'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
# change NICK below for your botnick
irc.send ( 'NICK EJGithub\n' )
# change USER below for user name. Keep Layout the same
irc.send ( 'USER ejgit ejgit ejgit :EJGithub\n' )
# change JOIN below for your pools IRC channel
irc.send ( 'JOIN #elitist\n' )
last_fast_check = datetime.datetime.now()

while True:
    data = irc.recv ( 4096 )
    print data
    if data.find ( 'PING' ) != -1:
        irc.send ( 'PONG ' + data.split() [ 1 ] + '\n' )


#Change channel #elitist to your pools IRC Channel (2 Locations of #elitist)
    if data.find('#elitist :!help') != -1:
        irc.send ( 'PRIVMSG #elitist : Elitist Bot Commands. !status !last !ticker !u !donations \n')
        
#Change channel #elitist and also Pool Donations address (2 Locations of #elitist)       
    if data.find('#elitist :!donations') != -1:
        irc.send ( 'PRIVMSG #elitist : Pool Donations change_this_to_your_ltc_address | Bot Donations goes to WKNiGHT at LewixZv4FMuz5dzxUqrH9P1SR2DvaxTmef \n')

#Change channel #elitist and also urlopen to your api address (2 Locations of #elitist)
    if data.find('#elitist :!status') != -1:
            url = urllib.urlopen('http://www.ejpool.info/index.php?page=api&action=public')
            status = url.read()
            status = json.loads(status)
            print status['hashrate']
            print status['last_block']
            print status['shares_this_round']
            print status['workers']
            print status['pool_name']
            irc.send ( 'PRIVMSG #elitist :' + str(status['pool_name']) + ' Last Block: ' + str(status['last_block']) + ' | Shares This Round: ' + str(status['shares_this_round']) + ' | Current Hashrate: ' + str(status['hashrate']) + ' kh/s' +  ' | Currently '+ str(status['workers']) + ' workers' '\n')

#Change channel #elitist and also urlopen to your api address with your Account API KEY (2 Locations of #elitist)
    if data.find('#elitist :!last') != -1:
        url = urllib.urlopen('http://www.ejpool.info/index.php?page=api&action=getblocksfound&api_key=YOUR_API_ACCOUNT_KEY_HERE&limit=1')
        status = url.read()
        status = json.loads(status)
        print status['getblocksfound'][0]['id']
        print status['getblocksfound'][0]['height']
        print status['getblocksfound'][0]['confirmations']
        print status['getblocksfound'][0]['amount']
        print status['getblocksfound'][0]['time']
        print status['getblocksfound'][0]['difficulty']
        print status['getblocksfound'][0]['shares']
        print status['getblocksfound'][0]['finder']
        irc.send ( 'PRIVMSG #elitist :' + 'Last Block: #' + str(status['getblocksfound'][0]['height']) + ' | Shares: ' + str(status['getblocksfound'][0]['shares']) + ' | Confirmations: ' + str(status['getblocksfound'][0]['confirmations']) + ' | Solved By: ' + str(status['getblocksfound'][0]['finder']) + '\n')
        
#Change channel #elitist (2 Locations of #elitist)
    if data.find('#elitist :!ticker') != -1:
        url = urllib.urlopen('https://www.btc-e.com/api/2/10/ticker')
        data_parse = url.read()
        data_parse = json.loads(data_parse)
        print data_parse['ticker']['last']
        print data_parse['ticker']['high']
        print data_parse['ticker']['low']
        print data_parse['ticker']['avg']
        irc.send ( 'PRIVMSG #elitist :' + '[BTC-E/ticker] > Last: ' + str(data_parse['ticker']['last']) + ' | High: ' + str(data_parse['ticker']['high']) + ' | Low: ' + str(data_parse['ticker']['low']) + ' | Avg: ' + str(data_parse['ticker']['avg']) + '\n') 

#Change channel #elitist and also urlopen to your api address with your ADMIN API KEY (3 Locations of #elitist)
    if data.find('#elitist :!u') != -1:
        userCommand = data.split(':')[2]
        userNick = userCommand.split(' ')

        if len(userNick) == 2:
            userNick = userNick[1]
            url = urllib.urlopen('http://www.ejpool.info/index.php?page=api&action=getuserstatus&api_key=YOUR_ADMIN_API_KEY_HERE&id=' + userNick)
            data_parse = url.read()
            data_parse = json.loads(data_parse)
            print data_parse['getuserstatus']['username']
            print data_parse['getuserstatus']['hashrate']
            print data_parse['getuserstatus']['shares']
            print data_parse['getuserstatus']['shares']['valid']
            print data_parse['getuserstatus']['shares']['invalid']
            irc.send ( 'PRIVMSG #elitist :' + 'Username: ' + str(data_parse['getuserstatus']['username']) + ' | Hashrate: ' + str(data_parse['getuserstatus']['hashrate']) + ' kh/s' + ' | Shares Valid: ' + str(data_parse['getuserstatus']['shares']['valid']) + ' | Shares Invalid: ' + str(data_parse['getuserstatus']['shares']['invalid']) + '\n')


        else:
            print 'no user specified'
            irc.send ( 'PRIVMSG #elitist :' + 'User not known' + '\n')
 
#Change channel #elitist and also urlopen to your api address with your Account API KEY (2 Locations of #elitist            
    now = datetime.datetime.now()
    if last_fast_check < (now - datetime.timedelta(seconds=20*dbmult)):
        print 'Checking Pool for new blocks'
        last_block_check = datetime.datetime.now()
        url = urllib.urlopen('http://www.ejpool.info/index.php?page=api&action=getblocksfound&api_key=YOUR_ACCOUNT_API_KEY_HERE&limit=1')
        block = url.read()
        block = json.loads(block)
        block_height = str(block['getblocksfound'][0]['height'])
        try:
            print block['getblocksfound'][0]['id']
            print block['getblocksfound'][0]['height']
            print block['getblocksfound'][0]['confirmations']
            print block['getblocksfound'][0]['amount']
            print block['getblocksfound'][0]['time']
            print block['getblocksfound'][0]['difficulty']
            print block['getblocksfound'][0]['shares']
            print block['getblocksfound'][0]['finder']
            block_height = int(block['getblocksfound'][0]['height'])
            if prevblock_height == 0:
                prevblock_height = block_height
            elif prevblock_height != block_height:
 
                irc.send('PRIVMSG #elitist' +u' :BLOCK FOUND: ' + str(block['getblocksfound'][0]['height']) + ' | ' + str(block['getblocksfound'][0]['shares']) + ' shares | Amount: ' + str(block['getblocksfound'][0]['amount']) + ' | Found By ' + str(block['getblocksfound'][0]['finder']) + '\n') 
                prevblock_height = block_height
        except IOError, e:
            print e[0], e[1]
            errorcode_ltc = 1
            irc.send('#elitist','\x02\x034ERROR:  \x02\x030|\x034 Pool \x030|\x034 DOWN')
        except socket.error, e:
            print e
            errorcode_ltc = 1
            irc.send('#elitist','\x02\x034ERROR:  \x02\x030|\x034 Pool \x030|\x034 DOWN')
        else:
            if errorcode_ltc == 1:
                irc.send('#elitist','\x02\x033ONLINE: \x02\x030|\x033 Pool \x030|\x034 UP')
                errorcode_ltc = 0 
