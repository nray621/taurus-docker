from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from os import curdir, sep
import subprocess
import time

class S(BaseHTTPRequestHandler):
    def _set_response(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        if self.path.startswith("/run_test"):
            self._set_response('application/json')
            timestamp = {'xml_route': 'log/' + str(time.time()) + '.xml', 'csv_route': 'log/' + str(time.time()) + '.csv'}
            json_timestamp = json.dumps(timestamp)
            self.wfile.write(json_timestamp.encode('utf-8'))
            subprocess.run("bzt test.yml", shell=True)
            subprocess.run("touch {}".format(timestamp['xml_route']), shell=True)
            subprocess.run("touch {}".format(timestamp['csv_route']), shell=True)
            subprocess.run("mv results.xml {}".format(timestamp['xml_route']), shell=True)
            subprocess.run("mv results.csv {}".format(timestamp['csv_route']), shell=True)
        else:
            try:
                f = open(curdir + sep + self.path, 'rb')
                if self.path.endswith('csv'):
                    self._set_response('application/csv')
                else:
                    self._set_response('application/xml')
                self.wfile.write(f.read())
                f.close()
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        return

def run(server_class=HTTPServer, handler_class=S, port=8000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
