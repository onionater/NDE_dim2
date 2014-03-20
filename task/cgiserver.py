#!/usr/bin/env python
import sys
print sys.version
print sys.path
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
#import socket

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 8000)
handler.cgi_directories = ['/cgi-bin', '/htbin']
print "amy's server is serving... at http://localhost:8000"
#print 'hostname:'
#print socket.gethostname()
#print 'ip address:'
#print socket.gethostbyname(socket.gethostname())
httpd = server(server_address, handler)
httpd.serve_forever()