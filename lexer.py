'''
BFC.
Copyright (C) 2024  TheCodingCrafter

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from ply import lex

tokens = (
    'PLUS', 'MINUS', 'NUMBER', 'LEFT_BRACKET', 'RIGHT_BRACKET',
    'LESS_THAN', 'GREATER_THAN', 'COMMA', 'DOT'
)

t_PLUS     = r'\+'
t_MINUS    = r'-'
t_NUMBER   = r'[0-9]+'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_COMMA = r','
t_DOT = r'\.'



def t_COMMENT(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += len(t.value.split('\n'))

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_whitespace(t):
    r'[\s]+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(data):
    tokens_list = []
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break
        tokens_list.append(tok)
    return tokens_list

if __name__ == '__main__':
    data = "+5-2>1"
    tokens = tokenize(data)
    print(tokens)