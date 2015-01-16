import asyncore,smtpd,logging,datetime

## dummy server setting
hostname = ''
port = 8025

class MyDebuggingServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        # write any code dere.
        
        now = datetime.datetime.today()
        inheaders = 1
        lines = data.split('\n')
        print str(now) + ' Receive message'
        print '---------- MESSAGE FOLLOWS ----------'
        for line in lines:
            # headers first
            if inheaders and not line:
                print 'X-Peer:', peer[0]
                inheaders = 0
            print line
        print '------------ END MESSAGE ------------'

MyDebuggingServer((hostname, port), None)

print 'Server Starting...'
print '%s:%d listening...' % (hostname, port)
try:
    asyncore.loop()
except:
    print 'Server Stopped'
