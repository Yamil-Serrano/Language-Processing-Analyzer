import ply.lex as lex

syntax_errors = []  # Lista para almacenar errores léxicos

# Token List: Define all possible token types in the language
tokens = [
    'ID', 'ID_FUNC', 'NUMBER', 'STRING',
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

# Ignore whitespace characters (except newline which is handled separately)
t_ignore = ' \t\r'

# Track line numbers correctly
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Comment handling function: Ignore comments starting with //
def t_COMMENT(t):
    r'//.*'
    pass

def t_ID_FUNC(t):
    r'[A-Z][a-zA-Z0-9_\']*'
    t.type = reserved.get(t.value, 'ID_FUNC')
    return t

def t_ID(t):
    r'[a-z][a-zA-Z0-9_\']*'
    t.type = reserved.get(t.value, 'ID')
    return t 

# NUMBER: combinations of numbers from 1-9
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# String: Text between double quotes
# [^"] means match any character except double quote
def t_STRING(t):
    r'"[^"]*"'
    return t

# Delimiters (r means regex or regular expression)
def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_LBRACE(t):
    r'\['
    return t

def t_RBRACE(t):
    r'\]'
    return t

def t_COMMA(t):
    r','
    return t

def t_ASSIGN(t):
    r':='
    return t

# Operators
def t_EQUAL(t):
    r'='
    return t

def t_LESS(t):
    r'<'
    return t

def t_GREATER(t):
    r'>'
    return t

def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_TIMES(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'/'
    return t

def t_DOT(t):
    r'\.'
    return t

def t_AND(t):
    r'\&'
    return t

def t_OR(t):
    r'\|'
    return t

# Error handling: Detect and report illegal characters
def t_error(t):
    line_num = t.lexer.lineno
    error_msg = f"Syntax error on line {line_num}: Illegal character '{t.value[0]}'"
    if not any(err[0] == line_num for err in syntax_errors):
        syntax_errors.append((line_num, 0, error_msg))
    t.lexer.skip(1)

def find_column(token):
    last_cr = token.lexer.lexdata.rfind('\n', 0, token.lexpos)
    return token.lexpos - last_cr

# Build the lexer with line tracking enabled
lexer = lex.lex()

# Only execute this part when running scanner directly
if __name__ == "__main__":
    # Clear any previous errors
    syntax_errors.clear()
    
    # Lexical Analysis Process
    # 1. Open the test file
    try:
        textFile = open('Program_Test.txt', 'r')
        
        # 2. Read entire file content into a string
        data = textFile.read()
        textFile.close()
        
        # 3. Feed the data to the lexer
        lexer.input(data)
        
        # Reset line number
        lexer.lineno = 1
        
        # 4. Token Extraction Loop
        print("-----------------------------------------------------\nInitiating Scanner...")
        while True:
            # Get next token
            tok = lexer.token()
            
            # If no more tokens, break the loop
            if not tok:
                break
            
            # Print each recognized token
            print(tok)
        print("Finalizing Scanner.")
        
        # Print any lexical errors
        if syntax_errors:
            print("\nLexical errors found:")
            for line, col, msg in sorted(syntax_errors, key=lambda x: x[0]):
                print(f"- {msg}")
        
    except Exception as e:
        print(f"Error during scanning: {str(e)}")