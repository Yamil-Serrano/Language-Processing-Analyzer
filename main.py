from Scanner import lexer  # Import lexer from Scanner
import ply.yacc as yacc
from Scanner import syntax_errors as lexical_errors
from Parser import syntax_errors, main as parser_main  # Import from our improved parser
from interpreter import Interpreter
import json
import sys

def main():
    # Clear any previous errors
    lexical_errors.clear()
    syntax_errors.clear()
    
    # Run the parser main function to parse and check for syntax errors
    ast = parser_main()
    
    # If there were syntax errors, exit without interpreting
    if syntax_errors or lexical_errors:
        seen = set()
        print("\n---------------------------------------------------------------")
        # Sort errors by line number for clearer output
        all_errors = lexical_errors + syntax_errors
        for line, _, msg in sorted(all_errors, key=lambda x: x[0]):
            # Only show one error per line to avoid overwhelming the user
            if line not in seen:
                print(f"- {msg}")
                seen.add(line)
        print(f"\n\033[91mSYNTAX ERRORS DETECTED. Interpreter will not run.\033[0m")
        print("----------------------------------------------------------------\n")
        return
        
    # If the AST is valid, proceed with execution
    if ast:
        # Print the AST in a readable format
        print("-----------------------------------------------------\nAbstract Syntax Tree")
        print(json.dumps(ast, indent=2))
        
        # Create an interpreter and run it
        try:
            interpreter = Interpreter()
            print("\n-----------------------------------------------------\nProgram Execution outputs: ")
            output = interpreter.interpret(ast)
            print(f"Output: {output}")
            print(f"\033[92mInterpreter Execution Complete\033[0m\n-----------------------------------------------------\n")
        except Exception as e:
            print(f"\nRUNTIME ERROR: {str(e)}")
            print(f"\n\033[91mInterpreter Execution failed\033[0m\n-----------------------------------------------------\n")
    else:
        print("\n-----------------------------------------------------")
        print(f"\n\033[91mAST creation failed. Interpreter will not run.\033[0m")
        print("-----------------------------------------------------\n")


if __name__ == '__main__':
    main()