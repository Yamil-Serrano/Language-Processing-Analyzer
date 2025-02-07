import ply.lex as lex

# Token List: Define all possible token types in the language
tokens = [
    'IDENTIFIER', 'NUMBER', 'STRING',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 
    'COMMA', 'ASSIGN',
    'EQUAL', 'LESS', 'GREATER', 'PLUS', 'MINUS', 
    'TIMES', 'DIVIDE', 'DOT', 'AND', 'OR'
]

# Reserved words that have special meaning in the language
# Cannot be used as variable or function identifiers
reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'let': 'LET',
    'val': 'VAL',
    'func': 'FUNC',
    'end': 'END',
    'in': 'IN',
    'nil': 'NIL',
    'true': 'TRUE',
    'false': 'FALSE',
    'exec': 'EXEC'
}

# Add reserved to token list
tokens += list(reserved.values())

# Ignore whitespace characters
# A whitespace is one of the following characters: tab (ASCII 9, \t ), newline 
#(ASCII 10, \n ), carriage return (ASCII 13, \r ), space (ASCII 32)
t_ignore = ' \t\r\n'

# Comment handling function: Ignore comments starting with //
def t_COMMENT(t):
    r'//.*'
    pass

# Identifier: starts with lowercase/uppercase letter, followed by optional 
# combinations of letters, digits, underscores, or single quotes
# The t.type is updated based on the dictionary lookup:
# - If t.value exists as a key in 'reserved', use its corresponding value as the type
# - If t.value is not in 'reserved', keep it as 'IDENTIFIER'
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_\']*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# String: Text between double quotes
# [^"] means match any character except double quote
t_STRING = r'"[^"]*"'

# Delimiters (r means regex or regular expresion)
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\['
t_RBRACE = r'\]'
t_COMMA = r','
t_ASSIGN = r':='

# Operators
t_EQUAL = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_DOT = r'\.'
t_AND = r'\&'
t_OR = r'\|'


# Error handling: Detect and report illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Lexical Analysis Process
# 1. Open the test file
textFile = open('Program_Test.txt', 'r')

# 2. Read entire file content into a string
data = textFile.read()

# 3. Feed the data to the lexer
lexer.input(data)

# 4. Token Extraction Loop
while True:
    # Get next token
    # When you call tok = lexer.token(), PLY scans the input code and tests each 
    # regular expression (t_...) in the order they are defined. 
    # If an expression matches, it returns a LexToken object.
    tok = lexer.token()
    
    # If no more tokens, break the loop
    if not tok:
        break
    
    # Print each recognized token
    print(tok)