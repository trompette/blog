#!/usr/bin/env python

import BaseHTTPServer
import os
import SimpleHTTPServer

__dir__ = os.path.dirname(os.path.abspath(__file__))

os.chdir(os.path.join(__dir__, 'web'))

a = ("127.0.0.1", 8080)
h = SimpleHTTPServer.SimpleHTTPRequestHandler
s = BaseHTTPServer.HTTPServer(server_address=a, RequestHandlerClass=h)
s.serve_forever()
