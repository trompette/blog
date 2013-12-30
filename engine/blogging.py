from logging import getLogger
from templating import get_metadata

logger = getLogger('blog-engine')


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
        if name not in self.tags:
            self.tags[name] = {
                'name': name,
                'posts': [],
            }
        self.tags[name]['posts'].append(post)

    def list_posts(self):
        return reversed(self.posts.values())
