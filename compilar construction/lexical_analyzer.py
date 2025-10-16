#!/usr/bin/env python3
"""
Lexical Analyzer for Compiler Construction
Phase 1 - Functional Programming Approach
"""

import re
import sys
from typing import List, Tuple, Dict


# Define Token Types (Keywords, Operators, Delimiters, etc.)
TOKEN_TYPES = {
    'KEYWORDS': ['if', 'else', 'while', 'for', 'int', 'float', 'char', 'return', 
                 'void', 'main', 'include', 'define', 'struct', 'break', 'continue',
                 'switch', 'case', 'default', 'do', 'goto', 'sizeof', 'typedef',
                 'union', 'enum', 'static', 'extern', 'const', 'volatile', 'register',
                 'auto', 'signed', 'unsigned', 'long', 'short', 'double'],
    'OPERATORS': ['+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
                 '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '++', '--',
                 '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>='],
    'DELIMITERS': [';', ',', '(', ')', '{', '}', '[', ']', '.', ':', '?'],
    'PREPROCESSORS': ['#']
}

# Read the content of the file
def read_file(filename: str) -> str:
    """Read and return content of the input file."""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

# Remove comments from the source code
def remove_comments(source_code: str) -> Tuple[str, List[Tuple[str, int]]]:
    """Remove single and multiline comments from source code."""
    lines = source_code.split('\n')
    cleaned_lines = []
    errors = []
    in_multiline_comment = False
    multiline_comment_start = 0
    
    for line_no, line in enumerate(lines, 1):
        cleaned_line = ""
        i = 0
        while i < len(line):
            if not in_multiline_comment and line[i:i+2] == '/*':
                # Start of multiline comment
                in_multiline_comment = True
                multiline_comment_start = line_no
                i += 2
                continue
            if in_multiline_comment and line[i:i+2] == '*/':
                # End of multiline comment
                in_multiline_comment = False
                i += 2
                continue
            if in_multiline_comment:
                i += 1
                continue
            if line[i:i+2] == '//':
                # End of line comment
                break
            cleaned_line += line[i]
            i += 1
        cleaned_lines.append(cleaned_line)
    
    if in_multiline_comment:
        errors.append(("Un-terminated comment", multiline_comment_start))
    
    return '\n'.join(cleaned_lines), errors

# Check if the token is a valid identifier
def is_valid_identifier(token: str) -> bool:
    """Check if a token is a valid identifier."""
    return bool(token) and (token[0].isalpha() or token[0] == '_') and all(c.isalnum() or c == '_' for c in token[1:])

# Determine the type of a given token
def get_token_type(token: str) -> str:
    """Classify the token into its respective type (keyword, operator, etc.)."""
    if token in TOKEN_TYPES['KEYWORDS']:
        return 'KEYWORD'
    if token in TOKEN_TYPES['OPERATORS']:
        return 'OPERATOR'
    if token in TOKEN_TYPES['DELIMITERS']:
        return 'DELIMITER'
    if token in TOKEN_TYPES['PREPROCESSORS']:
        return 'PREPROCESSOR'
    if re.match(r'^[0-9]+$', token):
        return 'INT_CONST'
    if re.match(r'^[0-9]*\.[0-9]+$', token) or re.match(r'^[0-9]+\.[0-9]*$', token):
        return 'FLOAT_CONST'
    if re.match(r"^'.'$", token) or re.match(r"^'\\.'$", token):
        return 'CHAR_CONST'
    if re.match(r'^".*"$', token):
        return 'STRING_CONST'
    if is_valid_identifier(token):
        return 'IDENTIFIER'
    return 'UNKNOWN'

# Tokenize a single line of code
def tokenize_line(line: str, line_no: int) -> Tuple[List[Dict], List[Tuple[str, int]]]:
    """Tokenize a single line of source code."""
    tokens = []
    errors = []
    i = 0
    
    while i < len(line):
        if line[i].isspace():
            i += 1
            continue
        
        if line[i] == '"':
            # Handle string literals
            j = i + 1
            while j < len(line) and line[j] != '"':
                if line[j] == '\\' and j + 1 < len(line):
                    j += 2
                else:
                    j += 1
            if j < len(line):
                token = line[i:j+1]
                tokens.append({'token': token, 'lexeme': 'STRING_CONST', 'line_no': line_no})
                i = j + 1
            else:
                errors.append(("String constant exceeded line", line_no))
                break
            continue
        
        if line[i] == "'":
            # Handle character literals
            j = i + 1
            if j < len(line) and line[j] == '\\':
                j += 1  # Skip escape character
            if j < len(line):
                j += 1
            if j < len(line) and line[j] == "'":
                token = line[i:j+1]
                if len(token) > 4:
                    errors.append(("Char constant too long", line_no))
                else:
                    tokens.append({'token': token, 'lexeme': 'CHAR_CONST', 'line_no': line_no})
                i = j + 1
            else:
                errors.append(("Invalid character constant", line_no))
                i += 1
            continue
        
        if i < len(line) - 1:
            # Handle two-character operators
            two_char = line[i:i+2]
            if two_char in TOKEN_TYPES['OPERATORS']:
                tokens.append({'token': two_char, 'lexeme': 'OPERATOR', 'line_no': line_no})
                i += 2
                continue
        
        if line[i] in TOKEN_TYPES['OPERATORS'] + TOKEN_TYPES['DELIMITERS'] + TOKEN_TYPES['PREPROCESSORS']:
            # Handle one-character operators and delimiters
            tokens.append({'token': line[i], 'lexeme': get_token_type(line[i]), 'line_no': line_no})
            i += 1
            continue
        
        if line[i].isdigit():
            # Handle numeric constants (integers and floats)
            j = i
            has_dot = False
            while j < len(line) and (line[j].isdigit() or (line[j] == '.' and not has_dot)):
                if line[j] == '.':
                    has_dot = True
                j += 1
            token = line[i:j]
            token_type = 'FLOAT_CONST' if has_dot else 'INT_CONST'
            tokens.append({'token': token, 'lexeme': token_type, 'line_no': line_no})
            i = j
            continue
        
        if line[i].isalpha() or line[i] == '_':
            # Handle identifiers and keywords
            j = i
            while j < len(line) and (line[j].isalnum() or line[j] == '_'):
                j += 1
            token = line[i:j]
            token_type = get_token_type(token)
            tokens.append({'token': token, 'lexeme': token_type if token_type != 'IDENTIFIER' else 'ID', 'line_no': line_no})
            i = j
            continue
        
        # Handle unknown characters
        errors.append((f"Undefined symbol: {line[i]}", line_no))
        i += 1
    
    return tokens, errors

# Main lexical analysis function
def lexical_analyzer(source_code: str) -> Tuple[List[Dict], List[Tuple[str, int]]]:
    """Main function for lexical analysis."""
    cleaned_code, comment_errors = remove_comments(source_code)
    
    all_tokens = []
    all_errors = comment_errors.copy()
    
    # Process each line of the cleaned source code
    lines = cleaned_code.split('\n')
    for line_no, line in enumerate(lines, 1):
        if line.strip():  # Skip empty lines
            tokens, errors = tokenize_line(line, line_no)
            all_tokens.extend(tokens)
            all_errors.extend(errors)
    
    return all_tokens, all_errors

# Write the tokens and errors to an output file
def write_output(tokens: List[Dict], errors: List[Tuple[str, int]], output_file: str):
    """Write the lexical analysis results to a file."""
    with open(output_file, 'w') as f:
        f.write("TOKENS:\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Token':<20} {'Lexeme':<15} {'Line No':<10}\n")
        f.write("-" * 40 + "\n")
        for token in tokens:
            f.write(f"{token['token']:<20} {token['lexeme']:<15} {token['line_no']:<10}\n")
        
        if errors:
            f.write("\n" + "=" * 40 + "\n")
            f.write("ERRORS:\n")
            f.write("-" * 40 + "\n")
            for error, line_no in errors:
                f.write(f"Line {line_no}: {error}\n")

# Main function to run the lexical analyzer
def main():
    """Run the lexical analysis process."""
    input_file = input("Enter input file name: ")
    source_code = read_file(input_file)
    
    tokens, errors = lexical_analyzer(source_code)
    
    output_file = "lexical_output.txt"
    write_output(tokens, errors, output_file)
    
    print(f"Lexical Analysis Complete!")
    print(f"Tokens: {len(tokens)}")
    print(f"Errors: {len(errors)}")
    print(f"Results written to: {output_file}")

    # Display the results on the console
    print("\n" + "=" * 50)
    print("TOKENS:")
    print("-" * 50)
    print(f"{'Token':<20} {'Lexeme':<15} {'Line No':<10}")
    print("-" * 50)
    for token in tokens:
        print(f"{token['token']:<20} {token['lexeme']:<15} {token['line_no']:<10}")
    
    if errors:
        print("\n" + "=" * 50)
        print("ERRORS:")
        print("-" * 50)
        for error, line_no in errors:
            print(f"Line {line_no}: {error}")

if __name__ == "__main__":
    main()
