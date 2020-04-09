from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension, Markup
from jinja2.nodes import CallBlock, Const
from jinja2.utils import concat
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound
from yaml import load

from .highlighting import highlight_code
from .logging import logger


class HighlightExtension(Extension):
    tags = {'highlight'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        lang = Const(None)
        if not parser.stream.current.test('block_end'):
            lang = parser.parse_expression()
        call = self.call_method('_highlight', [lang])
        body = parser.parse_statements(['name:endhighlight'], drop_needle=True)

        return CallBlock(call, [], [], body).set_lineno(lineno)

    @staticmethod
    def _highlight(lang, caller):
        code = Markup(caller()).unescape()

        return highlight_code(code, lang)


def pygments_style(style):
    try:
        string = get_formatter_by_name('html', style=style).get_style_defs('.highlight')
    except ClassNotFound:
        logger.warning('Unknown Pygments style %s', style)
        string = '/* nothing */'

    return string


def get_environment(dirs):
    env = Environment(loader=FileSystemLoader(dirs),
                      extensions=[HighlightExtension])
    env.globals['pygments_style'] = pygments_style

    return env


def get_metadata(template, default={}):
    if 'metadata' in template.blocks:
        block_func = template.blocks['metadata']
        context = template.new_context()
        generator = block_func(context)
        metadata = load(concat(generator))
    else:
        metadata = default

    return metadata
