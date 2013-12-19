from jinja2 import Environment, FileSystemLoader
from jinja2_highlight import HighlightExtension
from pygments.formatters import get_formatter_by_name

def pygments_style(style):
    formatter = get_formatter_by_name('html', style=style)

    return formatter.get_style_defs('.highlight')

def getEnvironment(dirs):
    env = Environment(loader=FileSystemLoader(dirs),
                      extensions=[HighlightExtension])
    env.globals['pygments_style'] = pygments_style

    return env
