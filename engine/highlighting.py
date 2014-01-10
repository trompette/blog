from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

from .logging import logger


def highlight_code(code, lang):
    code = cleanup_code(code)

    try:
        lexer = get_lexer_by_name(lang, stripall=False)
    except ClassNotFound:
        logger.warning('Unknown Pygments language %s', lang)
        lexer = guess_lexer(code)

    return highlight(code, lexer, get_formatter_by_name('html'))


def cleanup_code(code):
    # removing empty ending lines
    code = code.rstrip()
    # replacing tabs by spaces
    code = code.expandtabs(4)
    # fixing indentation
    lines = code.splitlines()
    indent = min(map(lambda s: len(s)-len(s.lstrip(' ')) if s else float('inf'), lines))
    code = '\n'.join(map(lambda s: s[indent:] if s else '', lines))

    return code
