# LOLCode Interpreter

A comprehensive interpreter for the LOLCode esoteric programming language, developed as a project for CMSC 124 (Design and Implementation of Programming Languages) at the University of the Philippines Los Baños.

## Contributors

- **Gray Velkan Gonzales**
- **Yuuri Nonaka**
- **Paul Hadley Fababeir**

## Project Overview

This interpreter implements lexical, syntactical, and semantic analysis for LOLCode programs (.lol files). The project follows the specifications outlined in the CMSC 124 project requirements and aims to create a fully functional interpreter with a graphical user interface.

### Current Status: **Abstract Syntax Tree Complete**

- **Lexer**: Fully implemented and operational
- **Parser**: Complete syntax validation with AST construction
- **AST**: Complete node structure for all LOLCode constructs
- **Semantic Analyzer**: Basic symbol table construction implemented
- **GUI**: Integrated interface with all phases

## Project Structure

```
lolcode_interpreter/
├── lexer/
│   ├── __init__.py        # Package initializer - exports tokenize_program and TokenType
│   ├── lexer.py           # Main lexical analyzer
│   └── lol_tokens.py      # Token definitions, patterns, and human-readable descriptions
├── parser/
│   ├── __init__.py        # Package initializer - exports Parser, SyntaxError, and AST nodes
│   ├── parser.py          # Recursive-descent syntax analyzer with AST construction
│   └── ast_nodes.py       # AST node class definitions for all LOLCode constructs
├── semantics/
│   ├── __init__.py        # Package initializer - exports symbolize and get_value
│   └── symbolizer.py      # Symbol table construction and management
├── test_cases/
│   ├── 01_variables.lol   # Test: Variable declarations
│   ├── 02_gimmeh.lol      # Test: User input
│   └── ...                # Additional test files
├── contributors.txt       # List of contributing groupmates
├── lolcode_gui.py         # GUI application (main entry point)
├── README.md              # Project documentation and instructions
├── .gitignore
└── requirements.txt       # Project dependencies (if any)
```

## Installation & Setup

### Prerequisites
- Python 3.x (Python 3.7 or higher recommended)
- tkinter (usually included with Python installation)
- Windows, macOS, or Linux operating system

### Verifying Python Installation
```bash
python --version
# or
python3 --version
```

### Verifying tkinter Installation
```bash
python -m tkinter
```
A small window should appear if tkinter is properly installed.

### Installing tkinter (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
tkinter is typically included with Python. If needed:
```bash
brew install python-tk
```

**Windows:**
tkinter is included with the standard Python installer from python.org

## Running the Interpreter

### Method 1: Using the GUI (Recommended)

1. **Navigate to the project directory:**
```bash
cd path/to/lolcode_interpreter
```

2. **Run the GUI application:**
```bash
python lolcode_gui.py
```
or
```bash
python3 lolcode_gui.py
```

3. **Using the GUI:**
   - Click **File → Open** (or press `Ctrl+O`) to load a `.lol` file
   - Edit code directly in the text editor panel
   - Click **EXECUTE** to run lexical, syntax, and semantic analysis
   - View results in:
     - **Lexemes Table**: Tokenized output with classifications
     - **Symbol Table**: Variable declarations and values
     - **Console Output**: Analysis results and error messages

### Method 2: Command Line Interface

**Lexer only:**
```bash
python lexer/lexer.py test_cases/01_variables.lol
```

**With linebreaks shown:**
```bash
python lexer/lexer.py test_cases/01_variables.lol --show-linebreaks
```

**Parser with AST (Python script):**
```python
from lexer import tokenize_program
from parser import Parser, SyntaxError as LOLSyntaxError

# Read LOLCode file
with open('test_cases/01_variables.lol', 'r') as f:
    code = f.read()

# Tokenize
tokens = tokenize_program(code)

# Parse and build AST
try:
    parser = Parser(tokens)
    ast = parser.parse()
    print("Syntax is valid!")
    print(f"Program has {len(ast.statements)} statements")
except LOLSyntaxError as e:
    print(f"Error: {e}")
```

## Test Cases

The `test_cases/` directory contains various LOLCode programs for testing:

1. **01_variables.lol** - Variable declarations and initialization
2. **02_gimmeh.lol** - User input handling
3. **03_arithmetic.lol** - Arithmetic operations
4. **04_boolean.lol** - Boolean operations
5. **05_conditionals.lol** - If-else structures
6. **06_loops.lol** - Loop structures
7. **07_functions.lol** - Function definitions and calls
8. **Additional test files** - Edge cases and complex scenarios

### Running Test Cases

1. Launch the GUI: `python lolcode_gui.py`
2. Open a test file from the `test_cases/` directory
3. Click **EXECUTE**
4. Examine the output in all three panels:
   - Lexemes table (tokens)
   - Symbol table (variables)
   - Console (status and errors)

## GUI Features

### Main Interface Components

1. **Menu Bar**
   - File → Open (`Ctrl+O`)
   - File → Save (`Ctrl+S`)
   - File → Save As (`Ctrl+Shift+S`)

2. **Text Editor Panel** (Left)
   - Edit LOLCode source code
   - Syntax-aware editing area
   - Line numbering

3. **Lexemes Table** (Top Right)
   - Displays all tokens with human-readable classifications
   - Columns: Lexeme | Classification
   - Shows token types like "Code Delimiter", "Variable Declaration", etc.

4. **Symbol Table** (Bottom Right)
   - Shows declared variables and their values
   - Columns: Identifier | Value
   - Updates after semantic analysis

5. **Console Output** (Bottom)
   - Displays analysis results
   - Shows syntax errors with line numbers
   - Reports token and variable counts

6. **Execute Button**
   - Runs complete analysis pipeline
   - Lexical Analysis → Syntax Analysis → Semantic Analysis
   - Updates all display panels

### Keyboard Shortcuts
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file
- `Ctrl+Shift+S` - Save as new file

## Project Implementation Details

### Lexical Analysis (lexer/)

**Files:**
- `lexer.py` - Main tokenization engine
- `lol_tokens.py` - Token type definitions and patterns
- `__init__.py` - Package interface

**Key Features:**
- Pattern-based token recognition using regex
- Context-aware identifier classification
- Comment handling (single-line BTW and multi-line OBTW/TLDR)
- Line number tracking for error reporting
- Human-readable token descriptions for GUI display

**Token Types Include:**
- Code delimiters: `HAI`, `KTHXBYE`
- Variable operations: `I HAS A`, `ITZ`, `R`
- I/O operations: `VISIBLE`, `GIMMEH`
- Arithmetic operators: `SUM OF`, `DIFF OF`, `PRODUKT OF`, etc.
- Boolean operators: `BOTH OF`, `EITHER OF`, `NOT`, etc.
- Control flow: `O RLY?`, `WTF?`, loop constructs
- Function keywords: `HOW IZ I`, `I IZ`, `FOUND YR`
- Data types and literals: `NUMBR`, `NUMBAR`, `YARN`, `TROOF`

### Syntax Analysis (parser/)

**Files:**
- `parser.py` - Recursive-descent parser with AST construction
- `ast_nodes.py` - AST node class definitions
- `__init__.py` - Package interface

**Key Features:**
- Recursive-descent parsing (no parser generators used)
- Complete Abstract Syntax Tree construction
- Comprehensive syntax validation
- Detailed error messages with line numbers
- Support for all LOLCode constructs

**AST Node Types:**
- Program structure: `ProgramNode`
- Statements: `VariableDeclNode`, `AssignmentNode`, `VisibleNode`, `GimmehNode`
- Control flow: `ConditionalNode`, `SwitchNode`, `LoopNode`
- Functions: `FunctionDefNode`, `FunctionCallNode`, `ReturnNode`
- Expressions: `LiteralNode`, `BinaryOpNode`, `UnaryOpNode`, etc.

**Validation Includes:**
- Program structure (HAI/KTHXBYE boundaries)
- Variable declaration blocks (WAZZUP/BUHBYE)
- Statement syntax for all constructs
- Expression syntax and operator arity
- Control flow block structure
- Function definitions and calls
- Loop label matching

### Semantic Analysis (semantics/)

**Files:**
- `symbolizer.py` - Symbol table construction
- `__init__.py` - Package interface

**Key Features:**
- Symbol table generation from token stream
- Variable declaration tracking
- Variable initialization handling
- Implicit `IT` variable management

**Current Capabilities:**
- Tracks all declared variables
- Records variable values
- Handles declarations with and without initialization
- Special handling for `IT` variable

**Future Enhancements:**
- Migration to AST-based analysis
- Type checking and inference
- Scope management
- Full expression evaluation
- Runtime error detection

### Graphical User Interface (lolcode_gui.py)

**Implementation:**
- Built with Python's tkinter library
- Integrates all analysis phases
- Real-time token and symbol table display
- Console output for status and errors

**Class Structure:**
- `LOLCodeInterpreterGUI` - Main application class
- Methods for file operations, analysis execution, and display updates
- Event handlers for user interactions

## LOLCode Language Reference

### Basic Structure
```lolcode
HAI [version]
    [WAZZUP
        variable declarations
    BUHBYE]
    
    statements
KTHXBYE
```

### Variables
```lolcode
I HAS A varname              # Declaration
I HAS A varname ITZ value    # Declaration with initialization
varname R value              # Assignment
```

### Data Types
- `NOOB` - Uninitialized/null
- `NUMBR` - Integer (e.g., `42`, `-7`)
- `NUMBAR` - Float (e.g., `3.14`, `-2.5`)
- `YARN` - String (e.g., `"hello"`)
- `TROOF` - Boolean (`WIN` or `FAIL`)

### Operations
All operations use prefix notation:
```lolcode
SUM OF x AN y              # Addition
DIFF OF x AN y             # Subtraction
PRODUKT OF x AN y          # Multiplication
QUOSHUNT OF x AN y         # Division
MOD OF x AN y              # Modulo
BIGGR OF x AN y            # Maximum
SMALLR OF x AN y           # Minimum

BOTH OF x AN y             # AND
EITHER OF x AN y           # OR
WON OF x AN y              # XOR
NOT x                      # NOT
ALL OF x AN y AN z MKAY    # Multi-AND
ANY OF x AN y AN z MKAY    # Multi-OR

BOTH SAEM x AN y           # Equal
DIFFRINT x AN y            # Not equal
```

### Input/Output
```lolcode
VISIBLE expression         # Output
GIMMEH variable            # Input
```

### Control Flow
```lolcode
# If-Then-Else
O RLY?
    YA RLY
        statements
    MEBBE condition
        statements
    NO WAI
        statements
OIC

# Switch-Case
WTF?
    OMG value
        statements
    OMG value
        statements
    OMGWTF
        statements
OIC

# Loops
IM IN YR label operation YR variable [TIL|WILE condition]
    statements
IM OUTTA YR label
```

### Functions
```lolcode
HOW IZ I funcname [YR param1 [AN YR param2 ...]]
    statements
    FOUND YR expression
IF U SAY SO

I IZ funcname [YR arg1 [AN YR arg2 ...]] MKAY
```

### Comments
```lolcode
BTW This is a single-line comment

OBTW
This is a
multi-line comment
TLDR
```

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'tkinter'"**
- **Solution**: Install tkinter using your system's package manager (see Installation section)

**Issue: GUI doesn't launch**
- **Solution**: Verify Python version (3.7+) and tkinter installation
- Try: `python -m tkinter` to test tkinter

**Issue: "No such file or directory" when running lexer/parser**
- **Solution**: Ensure you're in the project root directory
- Check that file paths are correct

**Issue: Syntax errors not showing line numbers**
- **Solution**: This is a bug - report to the development team
- Workaround: Check the console output for detailed error messages

**Issue: Symbol table not updating**
- **Solution**: Ensure EXECUTE button is clicked after code changes
- Verify that variable declarations are in proper format

### Getting Help

If you encounter issues:
1. Check this README for solutions
2. Review test cases for correct LOLCode syntax
3. Examine console output for detailed error messages
4. Contact the development team (contributors listed above)

## Project Requirements Compliance

**No parser generators used** - All parsing is hand-written recursive-descent

**Custom lexical analyzer** - Pattern-based tokenization without external tools

**Custom syntax analyzer** - Recursive-descent parser from scratch

**GUI implementation** - tkinter-based interface with all required components

**Test cases included** - Comprehensive test suite in `test_cases/` directory

**Documentation** - Complete README with usage instructions

## Academic Integrity

This project was developed as coursework for CMSC 124 at the University of the Philippines Los Baños. All code is original work by the contributors listed above, following the course specifications and guidelines.

## License

This project is developed for educational purposes as part of CMSC 124 coursework at the University of the Philippines Los Baños.

---

**Course**: CMSC 124 - Design and Implementation of Programming Languages  
**Institution**: University of the Philippines Los Baños  
**Academic Year**: 2025-2026

For questions or issues, contact any of the contributors listed at the top of this document.
