from Scanner import tokens, lexer  # Import tokens from the lexer
import ply.yacc as yacc  # Import PLY's yacc module for parsing
import json  # For print the AST in the terminal
import sys   # For error handling and exit
from Scanner import syntax_errors as lexical_errors

# Global variable to track errors
syntax_errors = []  # Syntax errors

# Custom error class for syntax errors
class SyntaxErrorException(Exception):
    def __init__(self, message, lineno=None, lexpos=None, token=None):
        self.message = message
        self.lineno = lineno
        self.lexpos = lexpos
        self.token = token
        super().__init__(self.message)

# Operator precedence: Defines the order in which operators are evaluated
precedence = (
    ('left', 'OR'),  # OR has the lowest precedence
    ('left', 'AND'),  # AND has higher precedence than OR
    ('left', 'EQUAL', 'LESS', 'GREATER'),  # Comparison operators
    ('left', 'PLUS', 'MINUS'),  # Arithmetic
    ('left', 'TIMES', 'DIVIDE'),  # More arithmetic
    ('left', 'DOT'),  # Dot operator (e.g., object.member)
)

# Rules for programs without exec_line
def p_program_facts(p):
    'program : facts'
    p[0] = {'facts': p[1]}

# Rules for programs with exec_line
def p_program_facts_exec(p):
    'program : facts exec_line'
    p[0] = {'facts': p[1], 'stm': p[2]}

def p_facts_func_def(p):
    '''facts : func_def facts '''
    if p[2] == None:
        p[0] = {p[1]["name"] : p[1]}
    else:
        p[0] = {p[1]["name"] : p[1]} | p[2]
        
def p_facts_assign(p):
    '''facts : assign facts'''
    if p[2] == None:
        p[0] = {p[1]['name'] : p[1]}
    else:
        p[0] = {p[1]['name'] : p[1]} | p[2]

def p_facts_empty(p):
    '''facts : '''  # Empty production for facts
    p[0] = {}

def p_func_def(p):
    '''func_def : FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END'''
    p[0] = {
            'type': 'func',
            'name': p[2],
            'params': p[4],
            'stm': p[7]
        }

def p_params_ID_COMMA_params(p):
    '''params : ID COMMA params'''
    p[0] = [{'type': 'id', 'id': p[1]}] + p[3]
    
def p_params_ID_FUNC_COMMA_params(p):
    '''params : ID_FUNC COMMA params'''
    p[0] = [{'type': 'id_func', 'id_func': p[1]}] + p[3]
    
def p_params_ID(p):
    '''params : ID'''
    p[0] = [{'type': 'id', 'id': p[1]}]
    
def p_params_ID_FUNC(p):
    '''params : ID_FUNC'''
    p[0] = [{'type': 'id_func', 'id_func': p[1]}]

def p_assign(p):
    '''assign : VAL ID ASSIGN stm END'''
    p[0] = {
            'type': 'val',
            'name': p[2],
            'stm': p[4]
        }

def p_stm_function_call(p):
    '''stm : ID_FUNC LBRACE args RBRACE'''
    p[0] = {
        'type': 'stm_func_call',
        'id_func': p[1],
        'args': p[3]
    }

def p_args_multiple(p):
    '''args : stm COMMA args'''
    p[0] = [p[1]] + p[3]

def p_args_single(p):
    '''args : stm'''
    p[0] = [p[1]]

def p_args_ID_FUNC(p):
    '''args : ID_FUNC'''
    p[0] = [{'type': 'id_func', 'id_func': p[1]}]
    
def p_args_ID_FUNC_COMMA(p):
    '''args : ID_FUNC COMMA args'''
    p[0] = [{'type': 'id_func', 'id_func': p[1]}] + p[3]

# Binary operations
def p_stm_binary_op(p):
    '''stm : stm PLUS stm  
           | stm MINUS stm 
           | stm TIMES stm 
           | stm DIVIDE stm 
           | stm DOT stm 
           | stm LESS stm 
           | stm GREATER stm 
           | stm EQUAL stm 
           | stm AND stm 
           | stm OR stm'''
    p[0] = {
        'type': 'stm_op',
        'op': p[2],
        'value1': p[1],
        'value2': p[3]
    }

# Literal values
def p_stm_string(p):
    '''stm : STRING'''
    p[0] = {
        'type': 'stm_value',
        'type_value': 'string',
        'value': p[1]
    }

def p_stm_number(p):
    '''stm : NUMBER'''
    p[0] = {
        'type': 'stm_value',
        'type_value': 'number',
        'value': p[1]
    }

def p_stm_true(p):
    '''stm : TRUE'''
    p[0] = {
        'type': 'stm_value',
        'type_value': 'bool',
        'value': True
    }

def p_stm_false(p):
    '''stm : FALSE'''
    p[0] = {
        'type': 'stm_value',
        'type_value': 'bool',
        'value': False
    }

def p_stm_nil(p):
    '''stm : NIL'''
    p[0] = {
        'type': 'stm_value',
        'type_value': 'nil',
        'value': None
    }

def p_stm_id(p):
    '''stm : ID'''
    p[0] = {
        'type': 'stm_id',
        'id': p[1]
    }

# Grouped expression
def p_stm_paren(p):
    '''stm : LPAREN stm RPAREN'''
    p[0] = p[2]  # Direct evaluation, the parentheses are ignored

# If statement
def p_stm_if(p):
    '''stm : IF stm THEN stm ELSE stm END'''
    p[0] = {
        'type': 'stm_if',
        'condition': p[2],
        'then_stm': p[4],
        'else_stm': p[6]
    }

# Let statement
def p_stm_let(p):
    '''stm : LET facts IN stm END'''
    p[0] = {
        'type': 'stm_let',
        'facts': p[2],
        'stm': p[4]
    }

def p_exec_line(p):
    '''exec_line : EXEC stm'''
    p[0] = p[2]

# Enhanced error handling function
def p_error(p):
    global parser
    
    if p:
        line_num = p.lineno
        col_num = find_column(p)
        error_msg = f"Syntax error on line {line_num}"
        
        # Add error to our list if it's not already there
        if not any(err[0] == line_num for err in syntax_errors):
            syntax_errors.append((line_num, col_num, error_msg))
        
        # Error recovery - attempt to continue parsing
        parser.errok()
        
        # Skip to the next token that could start a valid production
        while True:
            tok = parser.token()
            if not tok or tok.type in ['END', 'VAL', 'FUNC', 'IF', 'LET', 'EXEC']:
                break
    else:
        # End of file error
        error_msg = "Syntax error at end of input"
        syntax_errors.append((999, 0, error_msg))  # Use high line number for EOF errors

def find_column(p):
    # Calculate the column number
    if p and hasattr(p.lexer, 'lexdata'):
        last_cr = p.lexer.lexdata.rfind('\n', 0, p.lexpos)
        if last_cr < 0:
            last_cr = 0
        return p.lexpos - last_cr
    return 0
        
# Main function to initiate parsing
def main():
    global parser
    
    # Clear any previous errors
    syntax_errors.clear()
    
    print("-----------------------------------------------------\nInitiating Parsing...")

    # Create parser with error recovery
    parser = yacc.yacc(debug=False, errorlog=yacc.NullLogger())

    try:
        with open('Program_Test.txt', 'r') as textFile:
            data = textFile.read()

        # Reset lexer for a clean start with proper line counting
        lexer.lineno = 1
        
        # Parse the data
        ast = parser.parse(data, lexer=lexer)
        
        # Combine lexical and syntax errors, ensure they're sorted by line number
        all_errors = lexical_errors + syntax_errors
        sorted_errors = sorted(all_errors, key=lambda x: x[0])
        
        if sorted_errors:
            print("\nParsing completed with errors:")
            for line, col, msg in sorted_errors:
                # For EOF errors, don't show the high line number
                if line == 999:
                    print(f"- {msg}")
                else:
                    print(f"- {msg}")
            print(f"\n\033[91m\nAST was not fully constructed due to errors.\033[0m")        
            return None
        else:
            print("Finalizing Parsing without any errors.")
            return ast
            
    except Exception as e:
        print(f"Error during parsing: {str(e)}")
        return None

# Run the main function
if __name__ == '__main__':
    main()