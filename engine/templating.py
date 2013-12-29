from logging import getLogger
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension, Markup
from jinja2.nodes import CallBlock, Const
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound
from yaml import load

logger = getLogger('blog-engine')


class HighlightExtension(Extension):
    tags = set(['highlight'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        lang = Const(None) if parser.stream.current.test('block_end') else parser.parse_expression()
        call = self.call_method('highlight_code', [lang])
        body = parser.parse_statements(['name:endhighlight'], drop_needle=True)

        return CallBlock(call, [], [], body).set_lineno(lineno)

    def highlight_code(self, lang, caller):
        code = self.cleanup_code(caller())
        try:
            lexer = get_lexer_by_name(lang, stripall=False)
        except ClassNotFound:
            logger.warning('Unknown Pygments language %s', lang)
            lexer = guess_lexer(code)

        return highlight(Markup(code).unescape(), lexer, get_formatter_by_name('html'))

    def cleanup_code(self, code):
        # removing empty ending lines
        code = code.rstrip()
        # replacing tabs by spaces
        code = code.expandtabs(4)
        # fixing indentation
        lines = code.splitlines()
        indent = min(map(lambda s: len(s)-len(s.lstrip(' ')) if s else float('inf'), lines))
        code = '\n'.join(map(lambda s: s[indent:] if s else '', lines))

        return code


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
        block = template.blocks['metadata']
        context = template.new_context()
        metadata = load(block(context).next())
    else:
        metadata = default

    return metadata
