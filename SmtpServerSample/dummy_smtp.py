import os
import asyncore
import smtpd
import datetime
import base64
import logging

# Dummy SMTP serer class.
class MyDebuggingServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        now = datetime.datetime.today()
        inheaders = 0
        b64encoding = 0
        
        # Separate mail header and body by empty line.
        lines = data.split('\n\n')
        
        headers = lines[0].split('\n')
        mail_body = lines[1].replace('\n', '')
        
        logging.info(str(now) + ' Receive message')
        logging.info('---------- MESSAGE FOLLOWS ----------')
        
        # Output mail header.
        for line in headers:
            # headers first
            if not inheaders and not line:
                logging.info('X-Peer:', peer[0])
                inheaders = 1
            
            if 'Content-Transfer-Encoding: base64' in line:
                b64encoding = 1
                
            logging.info(line)
        logging.info('')
        
        # If mail body base64 encoded, decode the string.
        if b64encoding:
          mail_body = base64.b64decode(mail_body)
        
        # Output mail body.
        logging.info(mail_body)
        logging.info('------------ END MESSAGE ------------')
        print


# Start the server.
script_dir = os.path.dirname(__file__)
logging.basicConfig(filename=script_dir + '/server.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

hostname = ''
port = 8025
MyDebuggingServer((hostname, port), None)

logging.info('Server Starting...')
logging.info('Listening at port :%d', port)

try:
    asyncore.loop()
except:
    logging.info('Server Stopped')
