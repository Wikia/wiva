# coding=utf-8
import logging
import pprint

__author__ = 'alistra'

import ply.yacc as yacc
# noinspection PyUnresolvedReferences
from wikitext.lexer import tokens


def p_empty(p):
    'empty :'
    pass


def p_article_empty(p):
    'article : empty'
    p[0] = []


def p_article_name(p):
    'article : article word'
    p[0] = p[1].append(p[2])


def p_word_name(p):
    'word : NAME'
    p[0] = p[1]

def p_word_square(p):
    'word : LSQUARE word RSQUARE'
    p[0] = p[2]


#
# def p_expression_plus(p):
#     'expression : expression PLUS term'
#     p[0] = p[1] + p[3]
#
#
# def p_expression_minus(p):
#     'expression : expression MINUS term'
#     p[0] = p[1] - p[3]
#
#
# def p_expression_term(p):
#     'expression : term'
#     p[0] = p[1]
#
#
# def p_term_times(p):
#     'term : term TIMES factor'
#     p[0] = p[1] * p[3]
#
#
# def p_term_div(p):
#     'term : term DIVIDE factor'
#     p[0] = p[1] / p[3]
#
#
# def p_term_factor(p):
#     'term : factor'
#     p[0] = p[1]
#
#
# def p_factor_num(p):
#     'factor : NUMBER'
#     p[0] = p[1]
#
#
# def p_factor_expr(p):
#     'factor : LPAREN expression RPAREN'
#     p[0] = p[2]
#


# Error rule for syntax errors
def p_error(p):
    pprint.pprint(p)
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc(start='article')


def parse(text):
    return parser.parse(text, debug=logging.getLogger())
