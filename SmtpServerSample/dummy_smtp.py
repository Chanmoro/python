import os
import asyncore
import smtpd
import datetime
import base64
import quopri
import logging

# Dummy SMTP serer class.
class MyDebuggingServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        now = datetime.datetime.today()
        inheaders = 0
        b64encoded = 0
        qpencoded = 0
        
        # Separate mail header and body by empty line.
        lines = data.split('\n\n')
        
        headers = lines[0].split('\n')
        mail_body = lines[1]
        
        logging.info(str(now) + ' Receive message')
        logging.info('---------- MESSAGE FOLLOWS ----------')
        
        # Output mail header.
        for line in headers:
            # headers first
            if not inheaders and not line:
                logging.info('X-Peer:', peer[0])
                inheaders = 1
            
            if 'Content-Transfer-Encoding: base64' in line:
                b64encoded = 1

            if 'Content-Transfer-Encoding: quoted-printable' in line:
                qpencoded = 1
                
            logging.info(line)
        
        logging.info('')
        
        # Decode the base64 encoded string.
        if b64encoded:
            mail_body = lines[1].replace('\n', '')
            mail_body = base64.b64decode(mail_body)
        
        # Decode the quoted-printable encoded string.
        if qpencoded:
            mail_body = lines[1].replace('\n', '')
            mail_body = quopri.decodestring(mail_body)
        
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
