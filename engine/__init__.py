__version__ = '0.1.0-dev'

from datetime import datetime
from os import listdir
from shutil import copytree, rmtree

from .blogging import Blog
from .logging import logger
from .rendering import render_blog_templates
from .templating import get_environment, get_metadata


class Engine(object):
    def __init__(self, pages_dir, posts_dir, templates_dir, build_dir, files_dir):
        self.pages_dir = pages_dir
        self.posts_dir = posts_dir
        self.build_dir = build_dir
        self.files_dir = files_dir
        self.environment = get_environment([pages_dir, posts_dir, templates_dir])
        self.blog = Blog()

    def start(self):
        logger.info('version %s', __version__)
        self.read_sources()
        self.rebuild_blog()

    def read_sources(self):
        logger.info('Reading pages in %s', self.pages_dir)
        for filename in listdir(self.pages_dir):
            pagename = filename[:-3]
            template = self.environment.get_template(filename)
            self.blog.add_page(pagename, template)

        logger.info('Reading posts in %s', self.posts_dir)
        for filename in listdir(self.posts_dir):
            postname = filename[:-3]
            template = self.environment.get_template(filename)
            metadata = {
                'title': filename[11:-8],
                'pubdate': datetime.strptime(filename[0:10], '%Y-%m-%d'),
                'tags': [],
                **get_metadata(template),
            }
            self.blog.add_post(postname, template, metadata)

    def rebuild_blog(self):
        logger.info('Flushing %s', self.build_dir)
        rmtree(self.build_dir)

        logger.info('Copying static files to %s', self.build_dir)
        copytree(self.files_dir, self.build_dir)

        logger.info('Rendering blog templates in %s', self.build_dir)
        render_blog_templates(self.blog, self.build_dir)
