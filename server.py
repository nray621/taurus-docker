from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import subprocess
import yaml

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        if self.path.startswith("/run_test"):
            concurrency_param = self.path.split('?concurrency=')
            if len(concurrency_param) > 1:
                self.wfile.write("running test with concurrency of {}".format(concurrency_param[1]).encode('utf-8'))
                subprocess.run("bzt test.yml -o execution.0.concurrency={}".format(concurrency_param[1]), shell=True)
            else:
                self.wfile.write(("running test").encode('utf-8'))
                subprocess.run("bzt test.yml", shell=True)
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        # self.wfile.write('')
        # self.copyfile(open('./stats.xml'), self.wfile)

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
