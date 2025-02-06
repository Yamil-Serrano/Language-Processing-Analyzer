# Language Processing Analyzer

This repository contains the development of a **Language Processing Analyzer**, structured into three phases. This document currently focuses on **Phase 1: Lexical Analysis**, with placeholders for the upcoming phases.

## Phase 1: Lexical Analysis

### 🔹 What is a Lexical Analyzer?
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

### 🔹 How does it work?
1. **Reads the source code.**
2. **Ignores whitespace and comments.**
3. **Identifies tokens according to lexical rules (regular expressions).**
4. **Generates a list of tokens.**
5. **Passes the tokens to the parser.**

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
🔜 **To be implemented in the next assignment.**

## Phase 3: Intermediate Code Generation
🔜 **To be implemented in the final assignment.**


