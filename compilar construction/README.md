# Lexical Analyzer - Compiler Construction Phase 1

A functional programming-based lexical analyzer for C programming language, developed as part of compiler construction coursework. This tool tokenizes C source code and identifies lexical errors.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Token Types](#token-types)
- [Installation](#installation)
- [Usage](#usage)
- [Input/Output Examples](#inputoutput-examples)
- [Error Detection](#error-detection)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This lexical analyzer is the first phase of a compiler that processes C source code and breaks it down into meaningful tokens. It follows functional programming principles and provides comprehensive error detection capabilities.

### What is a Lexical Analyzer?

A lexical analyzer (or lexer) is the first phase of a compiler that reads source code and converts it into tokens. Each token represents a meaningful unit in the programming language (keywords, identifiers, operators, etc.).

## ✨ Features

- **Tokenization**: Breaks down C source code into meaningful tokens
- **Comment Removal**: Handles both single-line (`//`) and multi-line (`/* */`) comments
- **Error Detection**: Identifies and reports lexical errors with line numbers
- **Multiple Token Types**: Recognizes keywords, operators, delimiters, constants, and identifiers
- **String & Character Literals**: Properly handles string and character constants
- **Preprocessor Support**: Recognizes preprocessor directives
- **Clean Output**: Generates formatted output with tokens and errors
- **Functional Approach**: Implements functional programming paradigm

## 🔤 Token Types

The analyzer recognizes the following token types:

### Keywords
```
if, else, while, for, int, float, char, return, void, main, include, define, 
struct, break, continue, switch, case, default, do, goto, sizeof, typedef, 
union, enum, static, extern, const, volatile, register, auto, signed, 
unsigned, long, short, double
```

### Operators
```
+, -, *, /, %, =, ==, !=, <, >, <=, >=, &&, ||, !, &, |, ^, ~, <<, >>, 
++, --, +=, -=, *=, /=, %=, &=, |=, ^=, <<=, >>=
```

### Delimiters
```
;, ,, (, ), {, }, [, ], ., :, ?
```

### Constants
- **Integer Constants**: `123`, `0`, `456`
- **Float Constants**: `3.14`, `0.5`, `2.0`
- **Character Constants**: `'a'`, `'Z'`, `'\n'`
- **String Constants**: `"Hello World"`, `"test"`

### Other
- **Identifiers**: Variable and function names (e.g., `count`, `message`)
- **Preprocessor**: `#` for preprocessor directives

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/CS-Fasih/LexicalAnalyzer-CompilerPhase1.git
cd LexicalAnalyzer-CompilerPhase1
```

2. No additional dependencies required! The analyzer uses only Python standard library.

## 💻 Usage

### Basic Usage

1. Prepare your C source code file (e.g., `input.c`)

2. Run the lexical analyzer:
```bash
python3 lexical_analyzer.py
```

3. Enter the input filename when prompted:
```
Enter input file name: input.c
```

4. The analyzer will:
   - Process the input file
   - Display token count and error count
   - Generate `lexical_output.txt` with detailed results
   - Print results to the console

### Command Line Example

```bash
$ python3 lexical_analyzer.py
Enter input file name: input.c
Lexical Analysis Complete!
Tokens: 46
Errors: 5
Results written to: lexical_output.txt
```

## 📊 Input/Output Examples

### Sample Input (`input.c`)

```c
/*
 * This is a multi-line comment
 * to test the lexical analyzer.
*/
int main() {
    int count = 100;
    string message = "Hello World!";
    char grade = 'A';

    if (count = 10) {
        /* A simple comment */
        count = count + 1;
    }

    // The following lines contain errors
    string bad_str = "this string never ends
    char bad_char = 'too_long';
    int invalid_#symbol = 5;
}

/* This comment is never closed.
```

### Sample Output (`lexical_output.txt`)

```
TOKENS:
----------------------------------------
Token                Lexeme          Line No   
----------------------------------------
int                  KEYWORD         5         
main                 KEYWORD         5         
(                    DELIMITER       5         
)                    DELIMITER       5         
{                    DELIMITER       5         
int                  KEYWORD         6         
count                ID              6         
=                    OPERATOR        6         
100                  INT_CONST       6         
;                    DELIMITER       6         
...

========================================
ERRORS:
----------------------------------------
Line 16: String constant exceeded line
Line 17: Char constant too long
Line 18: Undefined symbol: #
Line 21: Un-terminated comment
```

## ⚠️ Error Detection

The lexical analyzer detects the following types of errors:

| Error Type | Description | Example |
|------------|-------------|---------|
| **Un-terminated Comment** | Multi-line comment not closed | `/* comment` |
| **String Constant Exceeded Line** | String not closed on same line | `"unclosed string` |
| **Char Constant Too Long** | Character constant with multiple characters | `'abc'` |
| **Invalid Character Constant** | Malformed character literal | `'a` |
| **Undefined Symbol** | Unsupported character in code | `@`, `$` |

## 📁 Project Structure

```
LexicalAnalyzer-CompilerPhase1/
│
├── lexical_analyzer.py      # Main lexical analyzer implementation
├── input.c                   # Sample C source code input
├── lexical_output.txt        # Generated output with tokens and errors
└── README.md                 # Project documentation
```

### File Descriptions

- **`lexical_analyzer.py`**: Core implementation with functions for:
  - File reading
  - Comment removal
  - Tokenization
  - Error detection
  - Output generation

- **`input.c`**: Sample C code for testing the analyzer

- **`lexical_output.txt`**: Output file containing:
  - All identified tokens with their types and line numbers
  - All lexical errors with descriptions and line numbers

## 🔧 Implementation Details

### Key Functions

#### `read_file(filename: str) -> str`
Reads the input source file and returns its content.

#### `remove_comments(source_code: str) -> Tuple[str, List[Tuple[str, int]]]`
Removes single-line and multi-line comments from source code. Returns cleaned code and any comment-related errors.

#### `tokenize_line(line: str, line_no: int) -> Tuple[List[Dict], List[Tuple[str, int]]]`
Tokenizes a single line of code. Handles:
- String literals
- Character literals
- Multi-character operators
- Numeric constants
- Identifiers and keywords

#### `lexical_analyzer(source_code: str) -> Tuple[List[Dict], List[Tuple[str, int]]]`
Main analysis function that processes the entire source code.

#### `write_output(tokens: List[Dict], errors: List[Tuple[str, int]], output_file: str)`
Formats and writes tokens and errors to the output file.

### Algorithm Flow

```
1. Read source code from file
2. Remove all comments (single-line and multi-line)
3. Process each line:
   a. Identify string and character literals
   b. Recognize operators and delimiters
   c. Parse numeric constants
   d. Identify keywords and identifiers
   e. Detect invalid symbols
4. Collect all tokens and errors
5. Generate formatted output
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Potential Enhancements

- Add support for more C language features
- Implement symbol table generation
- Add support for preprocessor directive expansion
- Include more detailed error messages
- Add support for C++ tokens
- Create a GUI interface

## 📝 License

This project is developed as part of an academic course in Compiler Construction.

## 👨‍💻 Author

**Muhammad Fasih**
- GitHub: [@CS-Fasih](https://github.com/CS-Fasih)

## 🎓 Academic Context

This lexical analyzer is Phase 1 of a multi-phase compiler construction project. It demonstrates:
- Understanding of lexical analysis principles
- Implementation of tokenization algorithms
- Error detection and reporting
- Functional programming concepts in compiler design

## 📚 References

- Compilers: Principles, Techniques, and Tools (Dragon Book)
- Modern Compiler Implementation
- C Programming Language Specification

---

**Note**: This is an educational project for learning compiler construction concepts. It may not handle all edge cases of the complete C language specification.
