# coding=utf-8
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
    p[0] = p[1] + [p[2]]


def p_article_recursive_parens(p):
    'article : article LPAREN article RPAREN'
    p[0] = p[1] + [{"type": "in-parens", "value": p[3]}]


def p_article_recursive_square(p):
    'article : article LSBRACE article RSBRACE'
    p[0] = p[1] + [{"type": "in-square", "value": p[3]}]


def p_article_recursive_curly(p):
    'article : article LCBRACE article RCBRACE'
    p[0] = p[1] + [{"type": "in-curly", "value": p[3]}]


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
    return parser.parse(text, debug=logging.getLogger())
