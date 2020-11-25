from datetime import datetime
from feedgenerator import Rss201rev2Feed

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

    def generate_feed(self):
        feed = Rss201rev2Feed(
            title="Benoît Merlet's personal website",
            author_name="Benoît Merlet",
            link="https://www.chezmerlet.net/",
            description="Posts from a senior developer and FOSS enthusiast",
            language="en",
            feed_url="https://www.chezmerlet.net/feed.rss",
        )
        for post in self.posts.values():
            feed.add_item(
                unique_id=post['name'],
                title=post['metadata']['title'],
                link="https://www.chezmerlet.net/%s"%post['name'],
                description=post['template'].render(post=post),
                pubdate=post['metadata']['pubdate'],
            )

        return feed
