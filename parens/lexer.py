# coding=utf-8
__author__ = 'alistra'

# coding=utf-8
import re

tokens = (
    'TEXT', 'LPAREN', 'RPAREN', 'LSBRACE', 'RSBRACE', 'LCBRACE', 'RCBRACE'
)


def t_TEXT(t):
    r'[^\[\]\(\)\{\}]+'
    return t


def t_LPAREN(t):
    r'\('
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_LSBRACE(t):
    r'\['
    return t


def t_RSBRACE(t):
    r'\]'
    return t


def t_LCBRACE(t):
    r'\{'
    return t


def t_RCBRACE(t):
    r'\}'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex

lexer = lex.lex(reflags=re.UNICODE)


def tokenize(text):
    lexer.input(text)
    return list(lexer)
