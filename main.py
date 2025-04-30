from Scanner import lexer  # Import lexer from Scanner
import ply.yacc as yacc
from Parser import main as parser_main  # Import main function from Parser
from Parser import *  # Import parser rules and definitions
from interpreter import Interpreter
import json

def main():
    # Build the parser
    parser = yacc.yacc(debug=False)
    
    # Run the parser main function to display the AST
    parser_main()
    
    # Read input file
    with open('Program_Test.txt', 'r') as textFile:
        data = textFile.read()
    
    # Parse the content and get the AST
    ast = parser.parse(data, lexer=lexer)
    
    # Print the AST in a readable format
    print("\n------------------------------\nAbstract Syntax Tree")
    print(json.dumps(ast, indent=2) if ast else "AST is None (parsing failed)")
    
    # Create an interpreter and run it
    interpreter = Interpreter()
    print("\n------------------------------\nProgram Execution outputs: ")
    output = interpreter.interpret(ast)
    print(f"Output: {output}")
    
    print("\nInterpreter Execution Complete\n------------------------------\n")

if __name__ == '__main__':
    main()