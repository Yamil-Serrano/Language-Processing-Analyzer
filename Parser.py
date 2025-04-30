from Scanner import tokens, lexer  # Import tokens from the lexer
import ply.yacc as yacc  # Import PLY's yacc module for parsing
import json  # For print the AST in the terminal

# Operator precedence: Defines the order in which operators are evaluated
precedence = (
    ('left', 'OR'),  # OR has the lowest precedence
    ('left', 'AND'),  # AND has higher precedence than OR
    ('left', 'EQUAL', 'LESS', 'GREATER'),  # Comparison operators
    ('left', 'PLUS', 'MINUS'),  # Arithmetic
    ('left', 'TIMES', 'DIVIDE'),  # More arithmetic
    ('left', 'DOT'),  # Dot operator (e.g., object.member)
)

# Grammar rules with semantic actions
def p_global_facts(p):
    '''program : facts exec_line'''
    if len(p) == 2:
        p[0] = {'facts': p[1]} # Case when the code does not have an exec command
    else:
        p[0] = {'facts': p[1], 'stm': p[2]} # Case when the code has an exec command

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

# Error handling function
def p_error(p):
    if p:
        print(f"Syntax error at token: {p.type}, value: {p.value}")
    else:
        print("Syntax error at end of input.")

# Main function to initiate parsing
def main():
    print("\nInitiating Parsing:")

    # Build the parser
    parser = yacc.yacc(debug=False)

    # Read and parse the input file
    with open('Program_Test.txt', 'r') as textFile:
        data = textFile.read()

    # Parse the content and get the AST
    ast = parser.parse(data, lexer=lexer)

    # Print the AST in a readable format
    print("AST Structure:")
    print(json.dumps(ast, indent=2) if ast else "AST is None (parsing failed)")

    print("Finalizing Parsing")

# Run the main function
if __name__ == '__main__':
    main()