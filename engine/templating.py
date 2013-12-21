from logging import getLogger
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension, Markup
from jinja2.nodes import CallBlock, Const
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

logger = getLogger('blog-engine')

class HighlightExtension(Extension):
    tags = set(['highlight'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno

        if not parser.stream.current.test('block_end'):
            lang = parser.parse_expression()
        else:
            lang = Const(None)

        call = self.call_method('_highlight', [lang])
        body = parser.parse_statements(['name:endhighlight'], drop_needle=True)

        return CallBlock(call, [], [], body).set_lineno(lineno)

    def _highlight(self, lang, caller):
        code = caller()

        try:
            lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound:
            logger.warning('Unknown Pygments language %s', lang)
            lexer = guess_lexer(code)

        return highlight(Markup(code).unescape(), lexer, get_formatter_by_name('html'))

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
