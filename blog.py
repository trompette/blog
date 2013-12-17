#!/usr/bin/env python

import engine
import logging
import os

logging.basicConfig(level=logging.DEBUG)

engine\
    .Engine(pages_dir=os.path.join(os.getcwd(), 'pages'),
            posts_dir=os.path.join(os.getcwd(), 'posts'),
            templates_dir=os.path.join(os.getcwd(), 'templates'),
            web_dir = os.path.join(os.getcwd(), 'web'),
            logger=logging.getLogger('blog-engine'))\
    .start()
