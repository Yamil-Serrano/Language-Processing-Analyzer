from Lexical_Analyzer import tokens, lexer  # Import tokens from the lexer
import ply.yacc as yacc

# Operator precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'LESS', 'GREATER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'DOT'),
)

def p_global_facts(p):
    '''global_facts : facts exec_line '''
    pass

def p_facts(p):
    '''facts : func_def facts 
             | assign facts 
             | '''
    pass

def p_func_def(p):
    '''func_def : FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END'''
    pass

def p_params(p):
    '''params : ID_FUNC COMMA params 
              | ID COMMA params 
              | ID_FUNC 
              | ID '''
    pass

def p_assign(p):
    '''assign : VAL ID ASSIGN stm END'''
    pass

def p_stm_function_call(p):
    '''stm : ID_FUNC LBRACE args RBRACE '''
    pass

def p_args(p):
    '''args : ID_FUNC COMMA args 
            | stm COMMA args 
            | ID_FUNC 
            | stm'''
    pass

def p_stm(p):
    '''stm : stm PLUS stm  
            | stm MINUS stm 
            | stm TIMES stm 
            | stm DIVIDE stm 
            | stm DOT stm 
            | stm LESS stm 
            | stm GREATER stm 
            | stm EQUAL stm 
            | stm AND stm 
            | stm OR stm 
            | STRING 
            | NUMBER 
            | TRUE 
            | FALSE 
            | NIL 
            | ID 
            | LPAREN stm RPAREN 
            | IF stm THEN stm ELSE stm END 
            | LET facts IN stm END'''
    pass

def p_exec_line(p):
    '''exec_line : EXEC stm '''
    pass

def p_error(p):
    if p:
        print(f"Syntax error in input: {p.value} at line {p.lineno}")
    else:
        print("Syntax error in input: none.")

def main():
    print("Initiating Parsing")

    # Build the parser
    parser = yacc.yacc()

    # Read test file
    with open('Program_Test.txt', 'r') as textFile:
        data = textFile.read()

    # Parse the content
    parser.parse(data, lexer=lexer)

    print("Finalizing Parsing")

if __name__ == '__main__':
    main()
