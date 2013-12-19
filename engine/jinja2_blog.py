from logging import getLogger
from jinja2 import Environment, FileSystemLoader
from jinja2_highlight import HighlightExtension
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound

logger = getLogger('blog-engine')

def pygments_style(style):
    try:
        string = get_formatter_by_name('html', style=style).get_style_defs('.highlight')
    except ClassNotFound:
        logger.warning('Unknown Pygments style %s', style)
        string = '/* nothing */'

    return string

def getEnvironment(dirs):
    env = Environment(loader=FileSystemLoader(dirs),
                      extensions=[HighlightExtension])
    env.globals['pygments_style'] = pygments_style

    return env
