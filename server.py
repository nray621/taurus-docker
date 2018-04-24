import SimpleHTTPServer
import SocketServer
import subprocess

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()

subprocess.call('bzt test.yml', shell=True)
