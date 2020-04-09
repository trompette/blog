__version__ = '0.0.1-dev'

from os import listdir
from shutil import copytree, rmtree

from .blogging import Blog
from .logging import logger
from .rendering import strategies
from .templating import get_environment


class Engine(object):
    def __init__(self, pages_dir, posts_dir, templates_dir, build_dir, files_dir):
        self.pages_dir = pages_dir
        self.posts_dir = posts_dir
        self.templates_dir = templates_dir
        self.build_dir = build_dir
        self.files_dir = files_dir
        self.environment = get_environment([pages_dir, posts_dir, templates_dir])
        self.blog = Blog()

    def read_pages(self):
        logger.info('Reading pages in %s', self.pages_dir)
        for page in listdir(self.pages_dir):
            self.blog.add_page(page[:-3], self.environment.get_template(page))

    def read_posts(self):
        logger.info('Reading posts in %s', self.posts_dir)
        for post in listdir(self.posts_dir):
            self.blog.add_post(post[:-3], self.environment.get_template(post))

    def copy_files(self):
        logger.info('Flushing %s', self.build_dir)
        rmtree(self.build_dir)
        logger.info('Copying static files from %s', self.files_dir)
        copytree(self.files_dir, self.build_dir)

    def render_pages(self):
        logger.info('Rendering pages in %s', self.build_dir)
        for page in self.blog.pages.values():
            strategy = page['metadata']['strategy']
            strategies[strategy](page, self)

    def start(self):
        logger.info('version %s', __version__)
        self.read_pages()
        self.read_posts()
        self.copy_files()
        self.render_pages()
