from logging import getLogger
from os.path import join

logger = getLogger('blog-engine')


def dump_file(engine, filename, template, vars={}):
    logger.debug('Dumping %s', filename)
    with open(join(engine.build_dir, filename), 'w') as f:
        f.write(template.render(vars))


def default_strategy(page, engine):
    dump_file(engine=engine,
              filename=page['name'],
              template=page['template'])


def blog_strategy(page, engine):
    dump_file(engine=engine,
              filename=page['name'],
              template=page['template'],
              vars={'blog': engine.blog})


def post_strategy(page, engine):
    for post in engine.blog.posts.itervalues():
        dump_file(engine=engine,
                  filename=post['name'],
                  template=post['template'])


strategies = {
    'default': default_strategy,
    'blog': blog_strategy,
    'post': post_strategy,
}
