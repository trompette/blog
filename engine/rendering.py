import os

def blog_strategy(page, engine):
    engine.logger.debug('Dumping %s', page['name'])
    with open(os.path.join(engine.web_dir, page['name']), 'w') as f:
        f.write(page['template'].render(blog=engine.blog))

def post_strategy(page, engine):
    for post in engine.blog.posts.itervalues():
        engine.logger.debug('Dumping %s', post['name'])
        with open(os.path.join(engine.web_dir, post['name']), 'w') as f:
            f.write(post['template'].render())

strategies = {
    'blog': blog_strategy,
    'post': post_strategy,
}