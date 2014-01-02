__version__ = '0.0.1-dev'

import blogging
import logging
import os
import rendering
import shutil
import templating

logger = logging.getLogger('blog-engine')


class Engine(object):
    def __init__(self, pages_dir, posts_dir, templates_dir, build_dir, files_dir):
        self.pages_dir = pages_dir
        self.posts_dir = posts_dir
        self.templates_dir = templates_dir
        self.build_dir = build_dir
        self.files_dir = files_dir
        self.environment = templating.get_environment([pages_dir, posts_dir, templates_dir])
        self.blog = blogging.Blog()

    def read_pages(self):
        logger.info('Reading pages in %s', self.pages_dir)
        for page in os.listdir(self.pages_dir):
            self.blog.add_page(page[:-3], self.environment.get_template(page))

    def read_posts(self):
        logger.info('Reading posts in %s', self.posts_dir)
        for post in os.listdir(self.posts_dir):
            self.blog.add_post(post[:-3], self.environment.get_template(post))

    def copy_files(self):
        logger.info('Flushing %s', self.build_dir)
        shutil.rmtree(self.build_dir)
        logger.info('Copying static files from %s', self.files_dir)
        shutil.copytree(self.files_dir, self.build_dir)

    def render_pages(self):
        logger.info('Rendering pages in %s', self.build_dir)
        for page in self.blog.pages.itervalues():
            strategy = page['metadata']['strategy']
            rendering.strategies[strategy](page, self)

    def start(self):
        logger.info('version %s', __version__)
        self.read_pages()
        self.read_posts()
        self.copy_files()
        self.render_pages()
