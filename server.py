import http.server
import socketserver
import subprocess
import json
import urllib.parse

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

# httpd = socketserver.TCPServer(("", PORT), Handler)

# print("serving at port", PORT)
# httpd.serve_forever()

# subprocess.call('bzt test.yml', shell=True)

class S(Handler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        print('in do_GET')
        self._set_headers()
        parsed_path = urllib.parse(self.path)
        request_id = parsed_path.path
        response = subprocess.check_output(["python", request_id])
        self.wfile.write(json.dumps(response))

    def do_POST(self):
        self._set_headers()
        parsed_path = urllib.parse(self.path)
        request_id = parsed_path.path
        response = subprocess.check_output(["python", request_id])
        self.wfile.write(json.dumps(response))

    def do_HEAD(self):
        self._set_headers()

def run(server_class=http.server.HTTPServer, handler_class=S, port=8000):
    print('in run')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
