__version__ = '0.0.1-dev'

import logging
import os
import rendering
import templating
import yaml

logger = logging.getLogger('blog-engine')


class Engine(object):
    def __init__(self, pages_dir, posts_dir, templates_dir, web_dir):
        self.pages_dir = pages_dir
        self.posts_dir = posts_dir
        self.templates_dir = templates_dir
        self.web_dir = web_dir
        self.environment = templating.get_environment([pages_dir, posts_dir, templates_dir])
        self.blog = Blog()

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


class Blog(object):
    def __init__(self):
        self.pages = {}
        self.posts = {}
        self.tags = {}

    def add_page(self, name, template):
        logger.debug('Adding page %s', name)
        metadata = get_metadata(template, {'strategy': 'default'})
        self.pages[name] = {
            'name': name,
            'metadata': metadata,
            'template': template,
        }

    def add_post(self, name, template):
        logger.debug('Adding post %s', name)
        metadata = get_metadata(template, {'tags': []})
        self.posts[name] = {
            'name': name,
            'metadata': metadata,
            'template': template,
        }
        for tag in metadata['tags']:
            self.add_tag(tag, name)

    def add_tag(self, name, post):
        logger.debug('Adding tag %s', name)
        if not name in self.tags:
            self.tags[name] = {
                'name': name,
                'posts': [],
            }
        self.tags[name]['posts'].append(post)


def get_metadata(template, default={}):
    if 'metadata' in template.blocks:
        block = template.blocks['metadata']
        context = template.new_context()
        metadata = yaml.load(block(context).next())
    else:
        metadata = default

    return metadata
