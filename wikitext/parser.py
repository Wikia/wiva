# coding=utf-8
import logging
import traceback

from termcolor import colored

__author__ = 'alistra'

import ply.yacc as yacc
# noinspection PyUnresolvedReferences
from wikitext.lexer import *


def p_empty(p):
    'empty :'
    return None


def p_article_empty(p):
    'article : empty'
    p[0] = []


def p_article_name(p):
    'article : article object'
    p[0] = p[1] + [p[2]]


def p_object_name(p):
    'object : NAME'
    p[0] = p[1]


def p_object_number(p):
    'object : NUMBER'
    p[0] = p[1]


def p_object_comma(p):
    'object : COMMA'
    p[0] = p[1]


def p_object_square2(p):
    'object : LSQUARE LSQUARE insidesquare2 RSQUARE RSQUARE'
    p[0] = {'type': "internal_link", 'value': p[2]}


def p_object_curly2_name(p):
    'object :  LCURLY LCURLY NAME RCURLY RCURLY'
    p[0] = {'type': "template", 'value': p[2]}


def p_object_curly2_name_args(p):
    'object : LCURLY LCURLY NAME PIPE pipelist RCURLY RCURLY'
    p[0] = {'type': "template", 'value': p[2]}


def p_object_paren_name_args(p):
    'object : LPAREN article RPAREN'
    p[0] = {'type': "template", 'value': p[2]}


def p_object_squote3_name(p):
    'object : SQUOTE SQUOTE SQUOTE NAME SQUOTE SQUOTE SQUOTE'
    pass


def p_insidesquare2_name(p):
    'insidesquare2 : NAME'


def p_insidesquare2_name_with_colon(p):
    'insidesquare2 : NAME COLON NAME'


def p_insidesquare2_name_with_pipe(p):
    'insidesquare2 : NAME COLON NAME PIPE pipelist'
    pass


def p_pipelist_recursive(p):
    'pipelist : pipelist PIPE article'
    p[0] = p[1] + [p[3]]


def p_pipelist_base(p):
    'pipelist : article'
    p[0] = [p[1]]


# Error rule for syntax errors
def p_error(p):
    MAX_CONTEXT = 50
    pos = p.lexpos
    prev_line_pos = lexer.lexdata.find('\n', max(pos - MAX_CONTEXT, 0), pos)
    next_line_pos = lexer.lexdata.find('\n', pos)
    if prev_line_pos == -1:
        prev_line_pos = 0

    if next_line_pos > pos + MAX_CONTEXT:
        next_line_pos = pos + MAX_CONTEXT

    print colored("Syntax error in input!", "red")
    print
    print colored(lexer.lexdata[prev_line_pos:next_line_pos], "yellow")
    print


# Build the parser
parser = yacc.yacc(start='article')


def parse(text):
    return parser.parse(text, lexer=lexer, debug=logging.getLogger())
