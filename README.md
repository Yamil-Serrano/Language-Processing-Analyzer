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
🔜 **To be implemented in the next assignment.**

## Phase 3: Intermediate Code Generation
🔜 **To be implemented in the final assignment.**


