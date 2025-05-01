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
            print("\nInterpreter Execution Complete\n-----------------------------------------------------\n")
        except Exception as e:
            print(f"\nRUNTIME ERROR: {str(e)}")
            print("Interpreter execution failed\n-----------------------------------------------------\n")
    else:
        print("\n-----------------------------------------------------")
        print("AST creation failed. Interpreter will not run.")
        print("-----------------------------------------------------\n")

def validate_syntax_only():
    """
    Function to validate syntax without executing the program
    """
    print("\nValidating syntax only...")
    lexical_errors.clear()
    syntax_errors.clear()
    
    ast = parser_main()
    
    if syntax_errors or lexical_errors:
        all_errors = lexical_errors + syntax_errors
        print(f"\nFailed: {len(all_errors)} syntax error(s) detected.")
        
        seen = set()
        for line, _, msg in sorted(all_errors, key=lambda x: x[0]):
            if line not in seen:
                print(f"- {msg}")
                seen.add(line)
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