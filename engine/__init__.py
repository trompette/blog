__version__ = '0.0.1-dev'

import blogging
import logging
import os
import rendering
import templating

logger = logging.getLogger('blog-engine')


class Engine(object):
    def __init__(self, pages_dir, posts_dir, templates_dir, web_dir):
        self.pages_dir = pages_dir
        self.posts_dir = posts_dir
        self.templates_dir = templates_dir
        self.web_dir = web_dir
        self.environment = templating.get_environment([pages_dir, posts_dir, templates_dir])
        self.blog = blogging.Blog()

    def read_pages(self):
        logger.info('Reading pages...')
        for page in os.listdir(self.pages_dir):
            self.blog.add_page(page[:-3], self.environment.get_template(page))

    def read_posts(self):
        logger.info('Reading posts...')
        for post in os.listdir(self.posts_dir):
            self.blog.add_post(post[:-3], self.environment.get_template(post))

    def render_pages(self):
        logger.info('Rendering pages...')
        for page in self.blog.pages.itervalues():
            strategy = page['metadata']['strategy']
            rendering.strategies[strategy](page, self)

    def start(self):
        self.read_pages()
        self.read_posts()
        self.render_pages()
