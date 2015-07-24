# coding=utf-8
import logging
import ply.yacc as yacc
from parens.result import *
from parens.lexer import *

__author__ = 'alistra'

validation = None
paren_stack = None


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


def p_article_recursive_square(p):
    'article : article LSBRACE seen_LSBRACE article RSBRACE seen_RSBRACE'
    node = SquareNode(p[3])
    node.line = p.lineno(3)
    node.pos = p.lexpos(3)
    p[0] = p[1] + [node]


def p_article_recursive_curly(p):
    'article : article LCBRACE seen_LCBRACE article RCBRACE seen_RCBRACE'
    node = CurlyNode(p[3])
    node.line = p.lineno(3)
    node.pos = p.lexpos(3)
    p[0] = p[1] + [node]

def p_seen_LSBRACE(p):
    'seen_LSBRACE :'
    paren_stack.append({'paren': '[', 'token': p.stack[-1]})


def p_seen_RSBRACE(p):
    'seen_RSBRACE :'
    del paren_stack[-1]


def p_seen_LCBRACE(p):
    'seen_LCBRACE :'
    paren_stack.append({'paren': '{', 'token': p.stack[-1]})


def p_seen_RCBRACE(p):
    'seen_RCBRACE :'
    del paren_stack[-1]


# Error rule for syntax errors
def p_error(p):
    try:
        stack_elem = paren_stack.pop(-1)
    except IndexError:
        validation.add_error("Closing %s missing an opening" % p.value, p.lexpos)
        return

    paren = stack_elem['paren']
    token = stack_elem['token']
    validation.add_error("Opening %s missing a closing" % paren, token.lexpos)


parser = yacc.yacc(start='article')


def parse(text, v):
    global validation, paren_stack
    validation = v
    paren_stack = []
    return parser.parse(text, debug=logging.getLogger(), tracking=True)
