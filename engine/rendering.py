from os.path import join

from .logging import logger


def render_blog_templates(blog, build_dir):
    logger.debug('Rendering pages')
    for page in blog.pages.values():
        dump_file(pathname=build_dir,
                  filename=page['name'],
                  content=page['template'].render(blog=blog))

    logger.debug('Rendering posts')
    for post in blog.posts.values():
        dump_file(pathname=build_dir,
                  filename=post['name'],
                  content=post['template'].render(post=post))


def dump_file(pathname, filename, content):
    logger.debug('Dumping %s', filename)
    with open(join(pathname, filename), 'w') as f:
        f.write(content)
