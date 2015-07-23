# coding=utf-8
import logging
from termcolor import colored

__author__ = 'alistra'

import ply.yacc as yacc
# noinspection PyUnresolvedReferences
from wikitext.lexer import *


def p_empty(p):
    'empty :'
    return None


def p_article_base(p):
    'article : empty'
    p[0] = []


def p_article_recursive(p):
    'article : article object'
    p[0] = p[1] + [p[2]]


def p_names_base(p):
    'names : NAME'
    pass


def p_names_recursive(p):
    """names : names NAME
             | names COLON
             | names SQUOTE
             | names NUMBER
             | names DASH
             | names DOT
             | names COMMA
             | LPAREN names RPAREN
    """
    pass


def p_object_misc(p):
    """object : htmltag
              | htmlcomment
              | header
              | bullet
              | names
              | link"""
    p[0] = p[1]


def p_bullet(p):
    """bullet : TIMES article"""


def p_header(p):
    """header : EQUALS names EQUALS
              | EQUALS EQUALS names EQUALS EQUALS
              | EQUALS EQUALS EQUALS names EQUALS EQUALS EQUALS
              | EQUALS EQUALS EQUALS EQUALS names EQUALS EQUALS EQUALS EQUALS
              | EQUALS EQUALS EQUALS EQUALS EQUALS names EQUALS EQUALS EQUALS EQUALS EQUALS
              | EQUALS EQUALS EQUALS EQUALS EQUALS EQUALS names EQUALS EQUALS EQUALS EQUALS EQUALS EQUALS
    """


def p_link(p):
    '''link : LSQUARE LSQUARE names RSQUARE RSQUARE
              | LSQUARE LSQUARE names PIPE pipelist RSQUARE RSQUARE'''
    p[0] = {'type': "internal_link", 'value': p[2]}


def p_object_curly2_name(p):
    'object :  LCURLY LCURLY names RCURLY RCURLY'
    p[0] = {'type': "template", 'value': p[2]}


def p_object_curly2_name_args(p):
    'object : LCURLY LCURLY names PIPE pipelisttemplate RCURLY RCURLY'
    p[0] = {'type': "template", 'value': p[2]}


def p_object_paren_name_args(p):
    'object : LPAREN article RPAREN'
    p[0] = {'type': "template", 'value': p[2]}


# def p_object_squote3_name(p):
#     'object : SQUOTE SQUOTE SQUOTE names SQUOTE SQUOTE SQUOTE'
#     pass
#
#
# def p_object_squote2_name(p):
#     'object : SQUOTE SQUOTE names SQUOTE SQUOTE'
#     pass
#
#
# def p_object_squote_name(p):
#     'object : SQUOTE names SQUOTE'
#     pass


def p_object_dquote_name(p):
    'object : DQUOTE names DQUOTE'
    pass


def p_htmltag(p):
    '''htmltag : LANGLE NAME attributes DIVIDE RANGLE
               | LANGLE NAME attributes RANGLE article LANGLE DIVIDE NAME RANGLE'''
    pass


def p_attributes_recursive(p):
    'attributes : attributes NAME EQUALS DQUOTE NAME DQUOTE'
    pass


def p_attributes_base(p):
    'attributes : empty'
    pass


def p_htmlcomment(p):
    'htmlcomment : LANGLE BANG DASH DASH article DASH DASH RANGLE'


def p_pipelisttemplate_recursive(p):
    'pipelisttemplate : pipelisttemplate PIPE names EQUALS article'
    p[0] = p[1] + [p[3]]


def p_pipelisttemplate_base(p):
    'pipelisttemplate : names EQUALS article'
    p[0] = [p[1]]


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
    return parser.parse(text, lexer=lexer, debug=logging.getLogger())
