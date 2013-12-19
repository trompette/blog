import logging
import os

logger = logging.getLogger('blog-engine')

def dump_file(engine, file, template, vars={}):
    logger.debug('Dumping %s', file)
    with open(os.path.join(engine.web_dir, file), 'w') as f:
        f.write(template.render(vars))

def default_strategy(page, engine):
    dump_file(engine=engine,
              file=page['name'],
              template=page['template'])

def blog_strategy(page, engine):
    dump_file(engine=engine,
              file=page['name'],
              template=page['template'],
              vars={'blog': engine.blog})

def post_strategy(page, engine):
    for post in engine.blog.posts.itervalues():
        dump_file(engine=engine,
                  file=post['name'],
                  template=post['template'])

strategies = {
    'default': default_strategy,
    'blog': blog_strategy,
    'post': post_strategy,
}
