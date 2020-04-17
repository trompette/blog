__version__ = '0.0.1-dev'

from os import listdir
from shutil import copytree, rmtree

from .blogging import Blog
from .logging import logger
from .rendering import strategies
from .templating import get_environment, get_metadata


class Engine(object):
    def __init__(self, pages_dir, posts_dir, templates_dir, build_dir, files_dir):
        self.pages_dir = pages_dir
        self.posts_dir = posts_dir
        self.build_dir = build_dir
        self.files_dir = files_dir
        self.environment = get_environment([pages_dir, posts_dir, templates_dir])
        self.blog = Blog()

    def read_sources(self):
        logger.info('Reading pages in %s', self.pages_dir)
        for filename in listdir(self.pages_dir):
            pagename = filename[:-3]
            template = self.environment.get_template(filename)
            metadata = get_metadata(template, {'strategy': 'default'})
            self.blog.add_page(pagename, template, metadata)

        logger.info('Reading posts in %s', self.posts_dir)
        for filename in listdir(self.posts_dir):
            postname = filename[:-3]
            template = self.environment.get_template(filename)
            metadata = get_metadata(template, {'tags': []})
            self.blog.add_post(postname, template, metadata)

    def rebuild_blog(self):
        logger.info('Flushing %s', self.build_dir)
        rmtree(self.build_dir)

        logger.info('Copying static files to %s', self.build_dir)
        copytree(self.files_dir, self.build_dir)

        logger.info('Rendering pages in %s', self.build_dir)
        for page in self.blog.pages.values():
            strategy = page['metadata']['strategy']
            strategies[strategy](page, self)

    def start(self):
        logger.info('version %s', __version__)
        self.read_sources()
        self.rebuild_blog()
