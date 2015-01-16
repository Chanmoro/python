from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import os
import logging

# Dummy Web serer class.
class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        f = open("get_response.json")
        response_body = f.read()

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.send_header('Content-length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body)
        logging.info('[Request method] GET')
        logging.info('[Request headers]\n' + str(self.headers))

    def do_POST(self):
        f = open("post_response.json")
        response_body = f.read()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/xml; charset=UTF-8')
        self.send_header('Content-length', len(response_body))
        self.end_headers()
        self.wfile.write(response_body)
        logging.info('[Request method] POST')
        logging.info('[Request headers]\n' + str(self.headers))

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        logging.info('[Request doby]\n' + post_body)


# Start the server.
script_dir = os.path.dirname(__file__)
logging.basicConfig(filename=script_dir + '/server.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

host = ''
port = 8880
httpd = HTTPServer((host, port), MyHTTPRequestHandler)

logging.info('Server Starting...')
logging.info('Listening at port :%d', port)

try:
    httpd.serve_forever()
except:
    logging.info('Server Stopped')

