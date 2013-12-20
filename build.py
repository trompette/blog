#!/usr/bin/env python

import engine
import logging
import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.DEBUG)

e = engine.Engine(pages_dir=os.path.join(__dir__, 'pages'),
                  posts_dir=os.path.join(__dir__, 'posts'),
                  templates_dir=os.path.join(__dir__, 'templates'),
                  web_dir=os.path.join(__dir__, 'web'))
e.start()
