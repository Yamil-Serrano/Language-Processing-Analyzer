# Simple interpreter for the language
class Interpreter:
    def __init__(self):
        self.global_env = {}  # Global environment for variables and functions
    
    def interpret(self, ast):
        """Main entry point of the interpreter"""
        if not ast:
            return None
        
        # Initialize the global environment with "facts" (variables and functions)
        if 'facts' in ast:
            self.global_env = ast['facts']
        
        # If there is a statement to execute
        if 'stm' in ast:
            return self.eval_statement(ast['stm'])
        return None
    
    def eval_statement(self, stm):
        """Evaluates a statement according to its type"""
        if not stm:
            return None
        
        stm_type = stm.get('type')
        
        # Literal values (numbers, strings, booleans, nil)
        if stm_type == 'stm_value':
            return stm['value']
        
        # Identifiers (variables)
        elif stm_type == 'stm_id':
            return self.eval_identifier(stm)
        
        # Binary operations
        elif stm_type == 'stm_op':
            return self.eval_operation(stm)
        
        # Conditionals (if-then-else)
        elif stm_type == 'stm_if':
            return self.eval_if(stm)
        
        # Let blocks (local variables)
        elif stm_type == 'stm_let':
            return self.eval_let(stm)
        
        # Function calls
        elif stm_type == 'stm_func_call':
            return self.eval_function_call(stm)
        
        # Function references
        elif stm_type == 'id_func':
            return stm['id_func']
        
        print(f"ERROR: Unknown statement type: {stm_type}")
        return None
    
    def eval_identifier(self, stm):
        """Looks up the value of an identifier in the environment"""
        identifier = stm['id']
        
        # Look in the global environment
        if identifier in self.global_env:
            val_node = self.global_env[identifier]
            if val_node.get('type') == 'val':
                return self.eval_statement(val_node.get('stm'))
        
        print(f"ERROR: Undefined identifier: {identifier}")
        return None
    
    def eval_operation(self, stm):
        """Evaluates a binary operation"""
        op = stm['op']
        left_value = self.eval_statement(stm['value1'])
        right_value = self.eval_statement(stm['value2'])
        
        # Basic type checking and performing the operation
        if op == '+':
            # Integers or floats
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value + right_value
            # Strings
            elif isinstance(left_value, str) and isinstance(right_value, str):
                return left_value + right_value
            else:
                print(f"ERROR: Incompatible types for '+': {type(left_value)} and {type(right_value)}")
        
        elif op == '-':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value - right_value
            else:
                print(f"ERROR: Incompatible types for '-': {type(left_value)} and {type(right_value)}")
        
        elif op == '*':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value * right_value
            else:
                print(f"ERROR: Incompatible types for '*': {type(left_value)} and {type(right_value)}")
        
        elif op == '/':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                if right_value == 0:
                    print("ERROR: Division by zero")
                    return None
                return left_value / right_value
            else:
                print(f"ERROR: Incompatible types for '/': {type(left_value)} and {type(right_value)}")
        
        elif op == '=':
            return left_value == right_value
        
        elif op == '<':
            return left_value < right_value
        
        elif op == '>':
            return left_value > right_value
        
        elif op == '&':
            return bool(left_value) and bool(right_value)
        
        elif op == '|':
            return bool(left_value) or bool(right_value)
        
        else:
            print(f"ERROR: Unknown operator: {op}")
        
        return None
    
    def eval_if(self, stm):
        """Evaluates an if-then-else expression"""
        condition = self.eval_statement(stm['condition'])
        
        # If the condition is true, evaluate the 'then' branch
        if condition:
            return self.eval_statement(stm['then_stm'])
        # Otherwise, evaluate the 'else' branch
        else:
            return self.eval_statement(stm['else_stm'])
    
    def eval_let(self, stm):
        """Evaluates a let block, creating a new environment"""
        # Save the current global environment
        old_env = self.global_env.copy()
        
        # Add new definitions to the global environment
        facts = stm['facts']
        self.global_env.update(facts)
        
        # Evaluate the statement in the new environment
        result = self.eval_statement(stm['stm'])
        
        # Restore the previous global environment
        self.global_env = old_env
        
        return result
    
    def eval_function_call(self, stm):
        """Evaluates a function call"""
        func_name = stm['id_func']
        args = stm['args']
        
        # Look for the function in the global environment
        if func_name not in self.global_env:
            print(f"ERROR: Undefined function: {func_name}")
            return None
        
        func_def = self.global_env[func_name]
        
        # Check that it is a function
        if func_def.get('type') != 'func':
            print(f"ERROR: {func_name} is not a function")
            return None
        
        # Check number of arguments
        params = func_def.get('params', [])
        if len(args) != len(params):
            print(f"ERROR: Function {func_name} expects {len(params)} arguments, but got {len(args)}")
            return None
        
        # Save the current global environment
        old_env = self.global_env.copy()
        
        # Create a new environment with the function parameters
        new_env = {}
        for i, param in enumerate(params):
            param_name = param.get('id') if 'id' in param else param.get('id_func')
            arg_value = self.eval_statement(args[i])
            new_env[param_name] = {'type': 'val', 'name': param_name, 'stm': {'type': 'stm_value', 'value': arg_value}}
        
        # Update the global environment with the parameters
        self.global_env.update(new_env)
        
        # Execute the function body
        result = self.eval_statement(func_def['stm'])
        
        # Restore the previous global environment
        self.global_env = old_env
        
        return result

# To test the interpreter
if __name__ == "__main__":
    print("Simple interpreter module loaded.")
