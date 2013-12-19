__version__ = '0.0.1-dev'

import jinja2_blog
import os
import rendering


class Engine(object):
    def __init__(self, pages_dir, posts_dir, templates_dir, web_dir, logger):
        self.pages_dir = pages_dir
        self.posts_dir = posts_dir
        self.templates_dir = templates_dir
        self.web_dir = web_dir
        self.environment = jinja2_blog.getEnvironment(dirs=[pages_dir, posts_dir, templates_dir])
        self.logger = logger
        self.blog = Blog(logger)

    def read_pages(self):
        self.logger.info('Reading pages...')
        for page in os.listdir(self.pages_dir):
            self.blog.add_page(page[:-3], self.environment.get_template(page))

    def read_posts(self):
        self.logger.info('Reading posts...')
        for post in os.listdir(self.posts_dir):
            self.blog.add_post(post[:-3], self.environment.get_template(post))

    def render_pages(self):
        self.logger.info('Rendering pages...')
        for page in self.blog.pages.itervalues():
            rendering.strategies[page['strategy']](page, self)

    def start(self):
        self.read_pages()
        self.read_posts()
        self.render_pages()


class Blog(object):
    def __init__(self, logger):
        self.logger = logger
        self.pages = {}
        self.posts = {}
        self.tags = {}

    def add_page(self, name, template):
        self.logger.debug('Adding page %s', name)
        strategy = getattr(template.module, 'strategy', 'default')
        self.pages[name] = {
            'name': name,
            'strategy': strategy,
            'template': template,
        }

    def add_post(self, name, template):
        self.logger.debug('Adding post %s', name)
        tags = getattr(template.module, 'tags', [])
        self.posts[name] = {
            'name': name,
            'tags': tags,
            'template': template,
        }
        for tag in template.module.tags:
            self.add_tag(tag, name)

    def add_tag(self, name, post):
        self.logger.debug('Adding tag %s', name)
        if not self.tags.has_key(name):
            self.tags[name] = {
                'name': name,
                'posts': [],
            }
        self.tags[name]['posts'].append(post)
