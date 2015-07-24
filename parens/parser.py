# coding=utf-8
from parens.result import *

__author__ = 'alistra'

# coding=utf-8
import logging
from termcolor import colored
import ply.yacc as yacc
# noinspection PyUnresolvedReferences
from parens.lexer import *


def p_empty(p):
    'empty :'
    return None


def p_article_base(p):
    'article : empty'
    p[0] = []


def p_article_recursive(p):
    'article : article TEXT'
    node = TextNode(p[2])
    node.line = p.lineno(2)
    node.pos = p.lexpos(2)
    p[0] = p[1] + [node]


def p_article_recursive_parens(p):
    'article : article LPAREN article RPAREN'
    node = ParenNode(p[3])
    node.line = p.lineno(3)
    node.pos = p.lexpos(3)
    p[0] = p[1] + [node]


def p_article_recursive_square(p):
    'article : article LSBRACE article RSBRACE'
    node = SquareNode(p[3])
    node.line = p.lineno(3)
    node.pos = p.lexpos(3)
    p[0] = p[1] + [node]


def p_article_recursive_curly(p):
    'article : article LCBRACE article RCBRACE'
    node = CurlyNode(p[3])
    node.line = p.lineno(3)
    node.pos = p.lexpos(3)
    p[0] = p[1] + [node]


# Error rule for syntax errors
def p_error(p):
    MAX_CONTEXT = 50
    pos = p.lexpos
    prev_line_pos = lexer.lexdata.find('\n', max(pos - MAX_CONTEXT, 0), pos)
    next_line_pos = lexer.lexdata.find('\n', pos)
    if prev_line_pos == -1:
        prev_line_pos = max(pos - MAX_CONTEXT, 0)

    if next_line_pos > pos + MAX_CONTEXT or next_line_pos == -1:
        next_line_pos = pos + MAX_CONTEXT

    print colored("Syntax error in input!", "red")
    print
    print colored(lexer.lexdata[prev_line_pos:next_line_pos], "yellow").encode('utf-8')
    print


# Build the parser
parser = yacc.yacc(start='article')


def parse(text):
    return parser.parse(text, debug=logging.getLogger(), tracking=True)
