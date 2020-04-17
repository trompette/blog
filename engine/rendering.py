from os.path import join

from .logging import logger


def dump_file(pathname, filename, content):
    logger.debug('Dumping %s', filename)
    with open(join(pathname, filename), 'w') as f:
        f.write(content)


def default_strategy(page, engine):
    dump_file(pathname=engine.build_dir,
              filename=page['name'],
              content=page['template'].render())


def blog_strategy(page, engine):
    dump_file(pathname=engine.build_dir,
              filename=page['name'],
              content=page['template'].render(blog=engine.blog))


def post_strategy(page, engine):
    for post in engine.blog.posts.values():
        dump_file(pathname=engine.build_dir,
                  filename=post['name'],
                  content=post['template'].render())


strategies = {
    'default': default_strategy,
    'blog': blog_strategy,
    'post': post_strategy,
}
