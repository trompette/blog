#!/usr/bin/env python

import argparse
import logging
import os

import engine

__dir__ = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='Tool to build the static blog.')
parser.add_argument('--debug', action='store_true', help='switch to debug mode')
parser.add_argument('--dir', default='web', help='change build directory (default: %(default)s)')

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

e = engine.Engine(pages_dir=os.path.join(__dir__, 'pages'),
                  posts_dir=os.path.join(__dir__, 'posts'),
                  templates_dir=os.path.join(__dir__, 'templates'),
                  build_dir=os.path.join(__dir__, args.dir),
                  files_dir=os.path.join(__dir__, 'files'))
e.start()
