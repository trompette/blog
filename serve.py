#!/usr/bin/env python3

import argparse
import http.server
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='Tool to serve the static blog.')
parser.add_argument('--dir', default='web', help='change build directory (default: %(default)s)')
parser.add_argument('--host', default='127.0.0.1', help='change host (default: %(default)s)')
parser.add_argument('--port', type=int, default=8080, help='change port (default: %(default)s)')

args = parser.parse_args()

os.chdir(os.path.join(__dir__, args.dir))

server = http.server.HTTPServer(server_address=(args.host, args.port),
                                RequestHandlerClass=http.server.SimpleHTTPRequestHandler)
server.serve_forever()
