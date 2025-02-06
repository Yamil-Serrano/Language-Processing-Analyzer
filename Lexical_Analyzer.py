import ply.lex as lex

# Token List: Define all possible token types in the language
tokens = [
    'IDENTIFIER', 'NUMBER', 'STRING',
    'IF', 'THEN', 'ELSE', 'LET', 'VAL', 'FUNC', 
    'END', 'IN', 'NIL', 'TRUE', 'FALSE', 'EXEC',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 
    'COMMA', 'ASSIGN',
    'EQUAL', 'LESS', 'GREATER', 'PLUS', 'MINUS', 
    'TIMES', 'DIVIDE', 'DOT', 'AND', 'OR'
]

# Ignore whitespace characters
# A whitespace is one of the following characters: tab (ASCII 9, \t ), newline 
#(ASCII 10, \n ), carriage return (ASCII 13, \r ), space (ASCII 32)
t_ignore = ' \t\r\n'

# Comment handling function: Ignore comments starting with //
def t_COMMENT(t):
    r'//.*'
    pass

# Token Matching Rules using Regular expresions
# Identifier: Start with letter, followed by letters, numbers, underscore, or single quote
t_IDENTIFIER = r'[a-zA-Z][a-zA-Z0-9_\']*'

# Number: One or more consecutive digits
t_NUMBER =  r'[0-9]+'

# String: Text between double quotes
#The ^ symbol inside the brackets NEGATES the set, meaning "any character except" the ones inside.
#In this case, [^"] means "any character except the double quotes."
t_STRING = r'"[^"]*"'

# Keywords: Exact string matching
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_LET = r'let'
t_VAL = r'val'
t_FUNC = r'func'
t_END = r'end'
t_IN = r'in'
t_NIL = r'nil'
t_TRUE = r'true'
t_FALSE = r'false'
t_EXEC = r'exec'

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