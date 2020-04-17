#!/usr/bin/env python3

import argparse
import functools
import logging
import os

import engine

__dir__ = os.path.dirname(os.path.abspath(__file__))
relative_dir = functools.partial(os.path.join, __dir__)

parser = argparse.ArgumentParser(description='Tool to build the static blog.')
parser.add_argument('--debug', action='store_true', help='switch to debug mode')
parser.add_argument('--dir', default='web', help='change build directory (default: %(default)s)')

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

e = engine.Engine(pages_dir=relative_dir('pages'),
                  posts_dir=relative_dir('posts'),
                  templates_dir=relative_dir('templates'),
                  build_dir=relative_dir(args.dir),
                  files_dir=relative_dir('files'))
e.start()
