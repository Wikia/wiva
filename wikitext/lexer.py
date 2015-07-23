# coding=utf-8
import re

tokens = (
    'NAME', 'NUMBER',
    'PLUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'DOT', 'COLON', 'SEMICOLON', 'PIPE', 'COMMA',
    'UNDERSCORE', 'DASH', 'BANG', 'HASH', 'PERCENT',
    'LPAREN', 'RPAREN', 'LSQUARE', 'RSQUARE', 'LCURLY', 'RCURLY', 'LANGLE', 'RANGLE', 'SQUOTE', 'DQUOTE',
)

# Tokens
t_COMMA = r'\,'
t_PIPE = r'\|'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_DOT = r'\.'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LANGLE = r'\<'
t_RANGLE = r'\>'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SQUOTE = r'\''
t_DQUOTE = r'\"'
t_UNDERSCORE = r'\_'
t_DASH = ur'-|\–|%s' % u'\u2013'
t_BANG = r'\!'
t_HASH = r'\#'
t_PERCENT = r'\%'

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_\.]*'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


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
