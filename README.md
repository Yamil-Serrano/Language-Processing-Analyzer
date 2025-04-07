# Language Processing Analyzer

This repository contains the development of a **Language Processing Analyzer**, structured into three phases. This document currently focuses on **Phase 1: Lexical Analysis**, with placeholders for the upcoming phases.

## Phase 1: Lexical Analysis

### What is a Lexical Analyzer?
A **Lexical Analyzer (Lexer)** is the first stage of a compiler or interpreter. Its function is to **take the source code as input and break it down into the smallest meaningful units, called tokens**.

**Example of source code:**
```c
int x = 10;
```
**Lexical Analyzer Output:**
```
TOKEN_KEYWORD(int)
TOKEN_IDENTIFIER(x)
TOKEN_OPERATOR(=)
TOKEN_NUMBER(10)
TOKEN_SYMBOL(;)
```
These tokens will be used in the next phase (**syntax analysis**) to verify the structure of the code.

### How does it work?
1. **Reads the source code.**
2. **Ignores whitespace and comments.**
3. **Identifies tokens according to lexical rules (regular expressions).**
4. **Generates a list of tokens.**
5. **Passes the tokens to the parser.**

### Understanding Greedy Regular Expressions
In lexical analysis, regular expressions are **greedy** by default, meaning they try to match the longest possible string that fits their pattern. Here's how it works:

1. The lexer starts at a position in the input.
2. It looks ahead character by character, trying to match the longest possible sequence.
3. When it can't match any more characters, it creates a token with the matched sequence.

**Example with numbers:**
```python
# For the regular expression '\d+' (one or more digits)
Input: "123abc"

Lexer process:
1. Starts at '1' → matches
2. Looks ahead to '2' → still matches
3. Looks ahead to '3' → still matches
4. Looks ahead to 'a' → doesn't match
5. Creates NUMBER token with "123"
```

This greedy behavior ensures that numbers like "123" are tokenized as a single NUMBER token (123) rather than three separate tokens (1, 2, 3).

## Automata and Regular Expressions
The **lexer** can be implemented using **Deterministic Finite Automata (DFA)**, generated from **Regular Expressions**.

**Example of a regular expression for identifiers:**
```
[a-zA-Z][a-zA-Z0-9_]*
```
This represents a **word that starts with a letter and can contain numbers and underscores**.

**Example of a DFA to recognize "if", "int", and "else":**
```
  (q0) -- 'i' --> (q1) -- 'f' --> (q2) [IF]
    |                        
    |-- 'n' --> (q3) -- 't' --> (q4) [INT]
    |-- 'e' --> (q5) -- 'l' --> (q6) -- 's' --> (q7) -- 'e' --> (q8) [ELSE]
```
This diagram shows how a DFA recognizes keywords by following transitions between states.

## Implementation with PLY
In this repository, a lexer is implemented using PLY, utilizing **regular expressions and functions in Python** to define tokens.

**Example of lexer code:**
```python
import ply.lex as lex

# Token list
tokens = ['IDENTIFIER', 'NUMBER', 'IF', 'ELSE', 'PLUS', 'EQUAL']

# Lexical rules
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'
t_IF = r'if'
t_ELSE = r'else'
t_PLUS = r'\+'
t_EQUAL = r'='

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()
```

## Phase 2: Syntax Analysis (Parser)

### What is a Syntax Analyzer (Parser)?
A **Syntax Analyzer (Parser)** is the second stage of a compiler or interpreter. Its function is to **verify the structure of the source code**, based on the grammar rules. The parser checks if the sequence of tokens (generated by the lexical analyzer) follows the syntax of the language.

For example, given the input:
```c
int x = 10;
```
The parser would check if this code follows the correct syntax for variable declaration and assignment in the language.

### How does it work?
1. **Receives tokens from the lexical analyzer.**
2. **Follows the grammar rules** to match the sequence of tokens.
3. **Generates a syntax tree** (Abstract Syntax Tree - AST) that represents the hierarchical structure of the code.
4. **Reports errors** if the code does not conform to the defined syntax.

### Understanding Grammar Rules
In a parser, the language syntax is defined by **Context-Free Grammar (CFG)**, which is a set of production rules that describe how tokens can be combined into valid statements. 

Here is an example of a simple grammar rule for a mathematical expression:
```
expression : term
           | expression PLUS term
           | expression MINUS term
```
This means that an expression can be a single term, or an expression followed by a `PLUS` or `MINUS` operator and another term.

### Implementing the Parser with PLY
In this repository, the parser is implemented using **PLY (Python Lex-Yacc)**, which is a library that helps implement lexers and parsers in Python. We define the grammar rules and the precedence of operators using **BNF (Backus-Naur Form)**, and then use **PLY's yacc** module to create the parser.

#### Example of Parser Code:

```python
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

# Additional grammar rules for parameters, statements, assignments, etc.
```

### Defining the Grammar
The syntax of the language is described through grammar rules that specify how different components of the language can be combined. Each rule is written as a function with the format `def p_rule_name(p):` where `p` represents the list of elements that match the rule.

For example, the rule for a function definition is written as:
```python
def p_func_def(p):
    '''func_def : FUNC ID_FUNC LBRACE params RBRACE ASSIGN stm END'''
    pass
```

### Operator Precedence
In the parser, we define **operator precedence** to ensure that operations like `+` and `-` are handled before `*` and `/`, and that logical operators like `AND` and `OR` have their own precedence. This helps avoid ambiguities in parsing.

```python
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'LESS', 'GREATER'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'DOT'),
)
```

### Error Handling
In the parser, we define an error function to handle syntax errors. If the input doesn't match any of the grammar rules, it will print an error message indicating the problem:

```python
def p_error(p):
    if p:
        print(f"Syntax error in input: {p.value} at line {p.lineno}")
    else:
        print("Syntax error in input: none.")
```

## Phase 3: Semantic Analysis  

### What is Semantic Analysis?  
**Semantic Analysis** is the third stage of a compiler/interpreter. While syntax analysis ensures the code is grammatically correct, semantic analysis verifies that the code **makes logical sense** according to the language rules. It checks:  
- **Type compatibility** (e.g., `5 + "text"` is invalid).  
- **Variable/function existence** (e.g., using undeclared variables).  
- **Scope rules** (e.g., accessing variables outside their scope).  
- **Function argument validity** (e.g., incorrect number/type of arguments).  

### How Does It Work?  
1. **Traverses the AST** generated by the parser.  
2. **Validates context-sensitive rules** using symbol tables and type-checking logic.  
3. **Annotates the AST** with type information and scope details.  
4. **Reports errors** for logical inconsistencies.  

---

### Example: Semantic Rules in Action  
#### Code Snippet  
```python  
x = 5 + 3  
```

**Step-by-Step Analysis**
1. **Variable Declaration Check**:
   * If the language requires explicit declarations, ensure `x` is declared before use.
2. **Type Checking**:
   * Verify `5` (integer) and `3` (integer) are compatible with the `+` operator.
3. **Result Assignment**:
   * Assign the result type (integer) to `x`.

**PLY Rule Explanation**
For the expression `5 + 3`, the parser rule might look like:
```python
def p_stm_binary_op(p):  
    '''stm : stm PLUS stm'''  
    p[0] = {  
        'type': 'binary_op',  
        'operator': p[2],  # '+' (p[2] is the PLUS token)  
        'left': p[1],      # Left operand (e.g., the AST node for 5)  
        'right': p[3],     # Right operand (e.g., the AST node for 3)  
        'data_type': None  # Placeholder for semantic analysis  
    }  
```

* `p[0]`: The parent node combining the operation.
* `p[1]` and `p[3]`: Child nodes representing the operands (`5` and `3`).
* During semantic analysis, `data_type` is updated to `int` after validation.

**Key Components**

**1. Symbol Tables**
Track variables, functions, and their metadata (type, scope, etc.). Example:
```python
let  
    val x = 10  # Symbol table entry: {name: 'x', type: 'int', scope: 'local'}  
in  
    x + "hello"  # Error: x (int) + "hello" (string) is invalid  
end  
```

**2. Type Checking**
* Ensures operations are valid for their operand types.
* Example error: `Type mismatch: int + string is not allowed`.

**3. Scope Management**
* Validates variable visibility.
* Example error: `Variable 'y' not declared in this scope`.

**Error Handling Examples**

| **Error Case** | **Error Message** |
|----------------|-------------------|
| `5 + "text"` | Type mismatch: int and string |
| `foo(1, 2)` (expects 1 arg) | Function 'foo' expects 1 argument |
| `y = 10` (undeclared `y`) | Undeclared variable 'y' |

**Integration with the Parser**
Semantic actions are embedded in parser rules. For example:
```python
def p_assign(p):  
    '''assign : VAL ID ASSIGN stm END'''  
    # Semantic check: Ensure ID is declared (if required)  
    # and the RHS type matches the LHS type.  
    p[0] = {  
        'type': 'assign',  
        'name': p[2],  
        'value': p[4],  
        'data_type': infer_type(p[4])  # Semantic annotation  
    }  
```

**Next Steps**
* **Intermediate Code Generation**: Convert the validated AST into an intermediate representation (e.g., three-address code).
```python
# Example intermediate code for 'x = 5 + 3'  
t1 = 5 + 3  
x = t1  
```