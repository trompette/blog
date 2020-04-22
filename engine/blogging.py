from .logging import logger


class Blog(object):
    def __init__(self):
        self.pages = {}
        self.posts = {}
        self.tags = {}

    def add_page(self, pagename, template):
        logger.debug('Adding page %s', pagename)
        self.pages[pagename] = {
            'name': pagename,
            'template': template,
        }

    def add_post(self, postname, template, metadata):
        logger.debug('Adding post %s', postname)
        self.posts[postname] = {
            'name': postname,
            'metadata': metadata,
            'template': template,
        }
        for tagname in metadata['tags']:
            self.add_tag(tagname, postname)

    def add_tag(self, tagname, postname):
        logger.debug('Adding tag %s to post %s', tagname, postname)
        if tagname not in self.tags:
            self.tags[tagname] = {
                'name': tagname,
                'posts': [],
            }
        self.tags[tagname]['posts'].append(postname)
