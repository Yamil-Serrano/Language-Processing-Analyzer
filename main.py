from Scanner import lexer  # Import lexer from Scanner
import ply.yacc as yacc
from Parser import main as parser_main, syntax_errors  # Import from our improved parser
from Parser import *  # Import parser rules and definitions
from interpreter import Interpreter
import json
import sys

def main():
    # Build the parser
    parser = yacc.yacc(debug=False)
    
    # Run the parser main function to parse and check for syntax errors
    ast = parser_main()
    
    # If there were syntax errors, exit without interpreting
    if syntax_errors:
        print("\n================================================================================")
        print(f"{'\033[91m'}SYNTAX ERRORS DETECTED. Interpreter will not run.")
        print(f"Found {len(syntax_errors)} syntax error(s). Please fix them and try again.{'\033[0m'}")
        print("================================================================================\n")
        return
    
    # If the AST is valid, proceed with execution
    if ast:
        # Print the AST in a readable format
        print("\n------------------------------\nAbstract Syntax Tree")
        print(json.dumps(ast, indent=2))
        
        # Create an interpreter and run it
        try:
            interpreter = Interpreter()
            print("\n------------------------------\nProgram Execution outputs: ")
            output = interpreter.interpret(ast)
            print(f"Output: {output}")
            print("\nInterpreter Execution Complete\n------------------------------\n")
        except Exception as e:
            print(f"\nRUNTIME ERROR: {str(e)}")
            print("Interpreter execution failed\n------------------------------\n")
    else:
        print("\n------------------------------")
        print("AST creation failed. Interpreter will not run.")
        print("------------------------------\n")

def validate_syntax_only():
    """
    Function to validate syntax without executing the program
    """
    print("\nValidating syntax only...")
    ast = parser_main()
    
    if syntax_errors:
        print(f"\nFailed: {len(syntax_errors)} syntax error(s) detected.")
        return False
    else:
        print("\nSuccess: No syntax errors detected!")
        return True

if __name__ == '__main__':
    # Check if the user wants to validate syntax only
    if len(sys.argv) > 1 and sys.argv[1] == '--check-syntax':
        validate_syntax_only()
    else:
        main()