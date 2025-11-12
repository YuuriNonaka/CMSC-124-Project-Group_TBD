# LOLCode Interpreter

A comprehensive interpreter for the LOLCode esoteric programming language, developed as a project for CMSC 124 (Design and Implementation of Programming Languages) at the University of the Philippines Los Baños.

## Project Overview

This interpreter implements lexical, syntactical, and semantic analysis for LOLCode programs (.lol files). The project follows the specifications outlined in the CMSC 124 project requirements and aims to create a fully functional interpreter with a graphical user interface.

### Current Status: **Syntax Analysis Complete** ✔

- **Lexer**: Fully implemented and operational ✅
- **Parser**: Complete syntax validation with detailed error reporting ✅
- **Semantic Analyzer**: Basic symbol table construction implemented ⚙️
- **GUI**: Integrated interface with all three phases ✅

## Project Structure

```
lolcode_interpreter/
├── lexer/
│   ├── __init__.py        # Package initializer - exports tokenize_program and TokenType
│   ├── lexer.py           # Main lexical analyzer
│   └── lol_tokens.py      # Token definitions, patterns, and human-readable descriptions
├── parser/
│   ├── __init__.py        # Package initializer - exports Parser and SyntaxError
│   └── parser.py          # Recursive-descent syntax analyzer
├── semantics/
│   ├── __init__.py        # Package initializer - exports symbolize and get_value
│   └── symbolizer.py      # Symbol table construction and management
├── test_cases/
│   ├── 01_variables.lol   # Test: Variable declarations
│   ├── 02_gimmeh.lol      # Test: User input
│   └── ...                # Additional test files
├── lolcode_gui.py         # GUI application
├── .gitignore
└── README.md
```

## Quick Start

### Running the GUI (Recommended)
```bash
python lolcode_gui.py
```

### Running Individual Components (CLI)

**Lexer:**
```bash
python lexer/lexer.py test_cases/01_variables.lol [--show-linebreaks]
```

**Parser:**
```python
from lexer import tokenize_program
from parser import Parser, SyntaxError as LOLSyntaxError

code = open('test_cases/01_variables.lol').read()
tokens = tokenize_program(code)

try:
    parser = Parser(tokens)
    parser.parse()
    print("✅ Syntax is valid!")
except LOLSyntaxError as e:
    print(f"❌ {e}")
```

## GUI Features

The graphical interface provides an integrated development environment for LOLCode:

### Functional Features ✅
- **Text Editor Panel** - Edit LOLCode source code with syntax support
- **File Operations** - Open, Save, and Save As functionality with keyboard shortcuts
- **Lexemes Table** - View tokenized output with human-readable classifications
- **Symbol Table Display** - Shows variable declarations and their current values
- **Syntax Validation** - Real-time syntax checking with detailed error messages
- **Console Output** - Displays analysis results, syntax errors, and execution status
- **File Path Display** - Shows currently loaded file

### Analysis Pipeline
When you click **EXECUTE**, the interpreter runs:
1. **Lexical Analysis** → Tokenizes the source code
2. **Syntax Analysis** → Validates program structure
3. **Semantic Analysis** → Builds symbol table and checks semantics

If syntax errors are found, they appear in the console with specific line numbers and helpful messages.

### Token Display Format
The lexemes table displays tokens with descriptive classifications:
- `HAI` → "Code Delimiter" (not "HAI")
- `I HAS A` → "Variable Declaration" (not "I_HAS_A")
- `VISIBLE` → "Output Keyword" (not "VISIBLE")
- `12` → "Integer Literal" (not "NUMBR Literal")

### Keyboard Shortcuts
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file
- `Ctrl+Shift+S` - Save as new file

## File Descriptions

### `lolcode_gui.py`
The main GUI application built with tkinter.

**Key Components:**
- **LOLCodeInterpreterGUI Class**: Main application class
  - `create_menu()` - Sets up File menu and keyboard shortcuts
  - `create_text_editor()` - Text editing area for LOLCode source
  - `create_lexemes_table()` - Displays tokens in a tabular format with human-readable descriptions
  - `create_symbol_table()` - Displays variable names and their values from semantic analysis
  - `create_bottom_section()` - EXECUTE button and console output area
  - `execute()` - Runs complete analysis pipeline (lexer → parser → semantics)
  - `open_file()` / `save_file()` / `save_file_as()` - File operations

**GUI Layout:**
```
┌──────────────────────────────────────────────────┐
│ File Menu                                         │
├──────────────────────────────────────────────────┤
│ File Path: (None)                                 │
├────────────────┬──────────────────┬───────────────┤
│               │    Lexemes       │  SYMBOL TABLE   │
│               ├──────────────────┤                 │
│               │ Lexeme | Class   │  Identifier|Value│
│  Text Editor  │ ──────────────── │  ─────────────── │
│               │  HAI   | Code    │  IT        |     │
│               │        | Delimiter│  x         | 5   │
│               │  ...   | ...     │  ...       | ... │
│               │                  │                 │
├───────────────┴──────────────────┴─────────────────┤
│                  [ EXECUTE ]                       │
├──────────────────────────────────────────────────┤
│ Console Output                                     │
│ ✅ Syntax check passed!                            │
│ Total tokens: 45                                   │
│ Variables declared: 5                              │
└──────────────────────────────────────────────────┘
```

### `parser/parser.py`
Implements recursive-descent syntax validation for LOLCode programs.

**Key Components:**
- **Parser Class**: Main parsing engine with token stream management
  - `parse()` - Entry point for full program validation
  - `parse_program()` - Validates HAI...KTHXBYE structure
  - `parse_main_body()` - Handles optional WAZZUP block and statements
  - `parse_statement()` - Dispatches to specific statement parsers
  - `parse_expression()` - Validates expressions with proper operator syntax
  - Control flow parsers: `parse_conditional()`, `parse_switch()`, `parse_loop()`
  - Function parsers: `parse_function_definition()`, `parse_function_call()`

**Custom Exception:**
- **SyntaxError**: Custom exception with line number tracking for detailed error reporting

**Validation Features:**
- Program structure (HAI/KTHXBYE)
- Variable declarations (WAZZUP/BUHBYE blocks)
- All statement types (VISIBLE, GIMMEH, assignments)
- Expression syntax (arithmetic, boolean, comparison)
- Control flow (conditionals, switches, loops)
- Functions (definitions and calls)
- Proper operator arity and argument separators

**Error Messages:**
```
Expected variable identifier after 'I HAS A' on line 12
Program must end with KTHXBYE on line 1
Loop label mismatch: started with 'loop' but ended with 'wrongloop' on line 8
Binary operator requires AN between operands on line 5
SMOOSH must end with MKAY on line 7
```

**Design for Future AST:**
The parser is structured to easily add Abstract Syntax Tree (AST) construction. Each parse method can be extended to return tree nodes instead of just validating.

### `semantics/symbolizer.py`
Implements symbol table construction and management for semantic analysis.

**Key Components:**
- **Symbol Table Structure**: Dictionary mapping variable names to their values
  - Tracks all declared variables
  - Special variable `IT` stores implicit expression results
  - Values stored as strings for display purposes

**Key Functions:**

1. **`get_value(tokens, symbol_table)`**
   - Helper function that converts token sequences into string values
   - Resolves variable references to their stored values
   - Handles literals (YARN, NUMBR, NUMBAR, TROOF) directly
   - Filters out string delimiters
   - Returns space-joined string representation

2. **`symbolize(tokens)`**
   - Main entry point for symbol table construction
   - Processes token stream to build symbol table
   - Initializes with implicit `IT` variable
   - Handles variable declarations and assignments:
     - `I HAS A <var> ITZ <value>` - Declaration with initialization
     - `I HAS A <var>` - Declaration without initialization (empty string)
     - `VISIBLE <expression>` - Updates IT variable with output value
   - Returns complete symbol table dictionary

**Current Capabilities:**
- Variable declaration tracking
- Variable initialization with values
- Expression value extraction
- VISIBLE statement tracking (stores in IT)

**Future Enhancements:**
- Assignment statements (`<var> R <value>`)
- Type inference and validation
- Scope management
- Expression evaluation

### `lexer/lol_tokens.py`
Defines the token types, regular expression patterns, and human-readable descriptions for LOLCode lexemes.

**Key Components:**
- **TokenType Enum**: Contains all token classifications including:
  - Program structure: `HAI`, `KTHXBYE`, `WAZZUP`, `BUHBYE`
  - Variable operations: `I_HAS_A`, `ITZ`, `R`
  - I/O: `VISIBLE`, `GIMMEH`
  - Arithmetic: `SUM_OF`, `DIFF_OF`, `PRODUKT_OF`, `QUOSHUNT_OF`, `MOD_OF`, `BIGGR_OF`, `SMALLR_OF`
  - Boolean: `BOTH_OF`, `EITHER_OF`, `WON_OF`, `NOT`, `ALL_OF`, `ANY_OF`
  - Comparison: `BOTH_SAEM`, `DIFFRINT`
  - Control flow: `O_RLY`, `YA_RLY`, `NO_WAI`, `OIC`, `WTF`, `OMG`, `OMGWTF`
  - Loops: `IM_IN_YR`, `IM_OUTTA_YR`, `UPPIN`, `NERFIN`, `TIL`, `WILE`
  - Functions: `HOW_IZ_I`, `IF_U_SAY_SO`, `I_IZ`, `FOUND_YR`
  - Data types: `NUMBR`, `NUMBAR`, `YARN`, `TROOF`, `NOOB`
  - Identifiers: `VARIDENT`, `FUNCIDENT`, `LABEL`
  - Special: `LINEBREAK`, `COMMENT`, `UNKNOWN`

- **TOKEN_DESCRIPTIONS**: Dictionary mapping TokenType enum values to human-readable descriptions for GUI display
  - Example: `TokenType.HAI: "Code Delimiter"`
  - Example: `TokenType.I_HAS_A: "Variable Declaration"`
  - Example: `TokenType.VISIBLE: "Output Keyword"`
  
- **TOKEN_PATTERNS**: List of (regex_pattern, TokenType) tuples ordered by specificity
  - Multi-word keywords are matched first (e.g., `I HAS A`, `SUM OF`)
  - Single keywords follow
  - Literals are matched before type keywords
  - Identifiers are matched last as a catch-all

- **COMPILED_PATTERNS**: Pre-compiled regex patterns for efficient matching

### `lexer/lexer.py`
Implements the lexical analysis engine that converts LOLCode source into tokens.

**Key Functions:**

1. **`remove_comments(line)`**
   - Strips single-line comments (BTW) from a line
   - Uses case-insensitive matching with word boundaries
   - Returns the line content before the comment

2. **`classify_identifier(prev_tokens)`**
   - Contextually determines if an identifier is a variable, function, or label
   - Examines the previous token to make classification:
     - After `HOW_IZ_I` → `FUNCIDENT` (function definition)
     - After `I_IZ` → `FUNCIDENT` (function call)
     - After `IM_IN_YR` → `LABEL` (loop start)
     - After `IM_OUTTA_YR` → `LABEL` (loop end)
     - Default → `VARIDENT` (variable identifier)

3. **`tokenize_line(line, line_num, all_tokens_so_far=None)`**
   - Tokenizes a single line of LOLCode
   - Processes characters left-to-right, attempting pattern matches
   - Tracks position in line and matches patterns from COMPILED_PATTERNS
   - Handles unknown tokens by grouping non-whitespace characters
   - Returns list of (lexeme, token_type, line_number) tuples

4. **`tokenize_program(source_code)`**
   - Main entry point for lexical analysis
   - Handles multi-line comments (OBTW...TLDR)
   - Processes the entire program line by line
   - Adds LINEBREAK tokens after each line (except the last)
   - Returns complete token list for the program

5. **`print_tokens_table(tokens, show_linebreaks=False)`**
   - Formats and displays tokens in a readable table
   - Columns: Lexeme | Classification | Line
   - Optional display of linebreak tokens
   - Shows token count and hidden linebreak count

6. **`analyze_file(filename, show_linebreaks=False)`**
   - Reads a .lol file and performs lexical analysis
   - Displays formatted token table
   - Handles file not found and general errors
   - Returns the token list

**CLI Usage:**
```bash
python lexer/lexer.py <filename.lol> [--show-linebreaks]
```

## LOLCode Language Specifications

### File Format
- Extension: `.lol`
- Structure: `HAI` ... `KTHXBYE`
- One statement per line (no soft command breaks required)
- Single whitespace between keywords assumed

### Comments
- Single-line: `BTW <comment>`
- Multi-line: `OBTW` ... `TLDR` (must be on separate lines)

### Variables
- Declared in `WAZZUP` ... `BUHBYE` section
- Declaration: `I HAS A <varname>`
- Initialization: `I HAS A <varname> ITZ <value>`
- Assignment: `<varname> R <value>`
- Implicit variable `IT` stores expression results

### Data Types
- `NOOB` - Uninitialized
- `NUMBR` - Integer (e.g., `42`, `-7`)
- `NUMBAR` - Float (e.g., `3.14`, `-2.5`)
- `YARN` - String (e.g., `"hello"`)
- `TROOF` - Boolean (`WIN` or `FAIL`)

### Operations (Prefix Notation)
- Arithmetic: `SUM OF`, `DIFF OF`, `PRODUKT OF`, `QUOSHUNT OF`, `MOD OF`
- Comparison: `BOTH SAEM`, `DIFFRINT`
- Boolean: `BOTH OF`, `EITHER OF`, `WON OF`, `NOT`
- Infinite arity: `ALL OF` ... `MKAY`, `ANY OF` ... `MKAY`, `SMOOSH`

### Control Flow
**If-Then:**
```lolcode
<expression>
O RLY?
  YA RLY
    <code>
  NO WAI
    <code>
OIC
```

**Switch-Case:**
```lolcode
WTF?
  OMG <literal>
    <code>
  OMGWTF
    <code>
OIC
```

**Loops:**
```lolcode
IM IN YR <label> <UPPIN|NERFIN> YR <var> <TIL|WILE> <expression>
  <code>
IM OUTTA YR <label>
```

### Functions
```lolcode
HOW IZ I <funcname> [YR <param1> [AN YR <param2> ...]]
  <code>
  FOUND YR <expression>
IF U SAY SO

I IZ <funcname> [YR <arg1> [AN YR <arg2> ...]] MKAY
```

## Implementation Notes

### Lexical Analysis Details

1. **Pattern Matching Order**: The lexer matches patterns in order of specificity to avoid ambiguity. Multi-word keywords are checked before single-word ones.

2. **Context-Aware Classification**: Identifiers are classified based on context (previous token) to distinguish between variables, functions, and loop labels.

3. **Comment Handling**: 
   - Single-line comments (BTW) can coexist with statements
   - Multi-line comments (OBTW/TLDR) must be on separate lines

4. **Whitespace**: 
   - Leading/trailing whitespace is stripped
   - Internal whitespace in YARN literals is preserved
   - Single whitespace between keywords is assumed

5. **Line Tracking**: Each token records its line number for error reporting

6. **Human-Readable Descriptions**: The `TOKEN_DESCRIPTIONS` dictionary maps internal token types to user-friendly names for GUI display, maintaining separation between internal representation and user interface.

### Syntax Analysis Details

1. **Recursive-Descent Parsing**: The parser uses recursive-descent techniques without any parser generators, as required by project specifications.

2. **Token Stream Management**:
   - Linebreak tokens are filtered out for cleaner parsing
   - Current position tracked with lookahead capability
   - Token consumption with type validation

3. **Error Reporting**:
   - All syntax errors include specific line numbers
   - Clear messages indicate what was expected vs. what was found
   - Examples: "Expected variable identifier after 'I HAS A' on line 12"

4. **Expression Parsing**:
   - Validates operator arity (binary operators require exactly 2 operands)
   - Ensures proper use of `AN` separator between operands
   - Checks for `MKAY` terminators in infinite arity operations
   - Handles nested expressions recursively

5. **Control Flow Validation**:
   - Ensures proper block structure (O RLY...OIC, WTF...OIC)
   - Validates loop label matching
   - Checks required clauses (YA RLY after O RLY?)

6. **Future AST Construction**:
   - Parser designed to easily extend with AST node creation
   - Each parse method can be modified to return tree nodes
   - Current structure provides foundation for interpretation phase

### Semantic Analysis Details

1. **Symbol Table Structure**: Uses a Python dictionary for variable storage
   - Key: variable name (string)
   - Value: variable value (string representation)
   - Special entry: `IT` for implicit results

2. **Variable Tracking**: 
   - Declarations are tracked immediately upon encountering `I HAS A`
   - Uninitialized variables default to empty string
   - Initialized variables store their converted value

3. **Value Resolution**: 
   - Literals are used directly
   - Variable references are resolved from the symbol table
   - String delimiters are filtered out during processing

4. **Current Limitations**:
   - No type checking or inference yet
   - Assignment statements (`R`) not yet implemented
   - No scope management (global scope only)
   - Expression evaluation is basic (string concatenation)

### GUI Integration

The GUI integrates all three analysis phases:
1. Adding project root to Python's module search path
2. Importing `tokenize_program()` from lexer package
3. Importing `Parser` and `SyntaxError` from parser package
4. Importing `symbolize()` from semantics package
5. Running complete pipeline: Lexer → Parser → Semantics
6. Displaying results and errors in console output
7. Filtering out LINEBREAK tokens for cleaner display

## Testing

Test cases are organized in the `test_cases/` directory, covering:
- Variable declarations and initialization
- User input (GIMMEH)
- Arithmetic operations
- Boolean operations
- Control flow structures
- Functions
- Edge cases and error conditions

### Testing with GUI
1. Launch `python lolcode_gui.py`
2. Open a test file from `test_cases/`
3. Click EXECUTE
4. View tokens in the Lexemes table with descriptive classifications
5. Check console for syntax validation results

### Testing Individual Components

**Lexer (CLI):**
```bash
python lexer/lexer.py test_cases/01_variables.lol
```

**Parser (Python):**
```python
from lexer import tokenize_program
from parser import Parser, SyntaxError as LOLSyntaxError

code = """HAI
I HAS A x ITZ 5
VISIBLE x
KTHXBYE"""

tokens = tokenize_program(code)

try:
    parser = Parser(tokens)
    parser.parse()
    print("✅ Syntax is valid!")
except LOLSyntaxError as e:
    print(f"❌ {e}")
```

**Symbol Table (Python):**
```python
from lexer import tokenize_program
from semantics import symbolize

code = """HAI
I HAS A x ITZ 5
VISIBLE x
KTHXBYE"""

tokens = tokenize_program(code)
symbol_table = symbolize(tokens)
print(symbol_table)  # {'IT': '5', 'x': '5'}
```

### Test Cases for Parser

**Valid syntax (should pass):**
```lolcode
HAI
WAZZUP
    I HAS A x ITZ 5
    I HAS A y
BUHBYE
VISIBLE x
x R 10
KTHXBYE
```

**Invalid syntax examples:**

1. **Missing KTHXBYE:**
```lolcode
HAI
VISIBLE "hello"
```
Error: `Program must end with KTHXBYE`

2. **Invalid variable declaration:**
```lolcode
HAI
WAZZUP
    I HAS A
BUHBYE
KTHXBYE
```
Error: `Expected variable identifier after 'I HAS A' on line 3`

3. **Unmatched loop labels:**
```lolcode
HAI
IM IN YR loop UPPIN YR x TIL BOTH SAEM x AN 10
    VISIBLE x
IM OUTTA YR wronglabel
KTHXBYE
```
Error: `Loop label mismatch: started with 'loop' but ended with 'wronglabel' on line 4`

4. **Missing MKAY:**
```lolcode
HAI
VISIBLE SMOOSH "hello" AN "world"
KTHXBYE
```
Error: `SMOOSH must end with MKAY on line 2`

5. **Missing AN separator:**
```lolcode
HAI
VISIBLE SUM OF 5 10
KTHXBYE
```
Error: `Binary operator requires AN between operands on line 2`

## Next Steps

### Phase 3: Complete Semantic Analysis - IN PROGRESS
- ✅ Symbol table construction
- ✅ Variable declaration tracking
- ⬜ Assignment statement handling (`<var> R <value>`)
- ⬜ Type checking and inference
- ⬜ Variable scope management
- ⬜ Full expression evaluation
- ⬜ Runtime error detection

### Phase 4: Abstract Syntax Tree (AST) - PLANNED
- Create AST node classes (ProgramNode, StatementNode, ExpressionNode, etc.)
- Modify parser to construct tree during validation
- Build tree structure representing program semantics
- Use AST for interpretation phase

### Phase 5: Interpreter/Executor - PLANNED
- Implement AST traversal and execution
- Handle I/O operations (VISIBLE, GIMMEH)
- Expression evaluation with type coercion
- Control flow execution
- Function calls and returns
- Connect to GUI console for output

### Phase 6: Complete GUI Implementation
- ✅ File explorer for loading .lol files
- ✅ Text editor for code viewing/editing
- ✅ Token list display with human-readable descriptions
- ✅ Symbol table display
- ✅ Console output for errors and messages
- ⬜ Interactive console for GIMMEH input
- ⬜ Program execution with runtime I/O

## Project Requirements

- **Prohibited**: No use of Flex/Lex, YACC/Bison, PEG, or any parser generator tools ✅
- **Required**: Custom implementation of lexical and syntax analyzers ✅
- **Evaluation**: Three progress presentations (lexer ✅, parser ✅, semantics ⚙️)
- **Minimum**: Interpreter must evaluate at least one operation/statement

## Development Guidelines

When continuing work on this codebase:

1. **Lexer is complete** ✅ - Fully functional and tested
2. **Parser is complete** ✅ - Validates all LOLCode syntax
3. **Semantic module started** 🔄 - Symbol table construction implemented
4. **GUI framework ready** - All phases integrated with console output
5. **Follow the pattern ordering** in `lol_tokens.py` - order matters!
6. **Context is key** - The `classify_identifier` function shows how to use previous tokens
7. **Test incrementally** - Use test cases to verify each feature
8. **Maintain token structure** - (lexeme, TokenType, line_number) tuples throughout
9. **Refer to specifications** - The project specs PDF contains authoritative rules
10. **Display layer separation** - `TokenType` for internal use; `TOKEN_DESCRIPTIONS` for GUI
11. **Module organization** - Keep lexer, parser, and semantics in separate packages
12. **Error handling** - Always provide line numbers and clear messages

### Common Issues to Watch

- Multi-word keywords must be matched before single-word components
- NOOB appears in both literals and type keywords - pattern order handles this
- Identifiers need contextual classification based on preceding tokens
- Linebreak tokens are added but filtered in parser
- GUI imports require project root in Python's path
- Token descriptions are purely for display - internal TokenType unchanged
- Import paths relative to project root (e.g., `from parser import Parser`)
- Custom SyntaxError imported as `LOLSyntaxError` to avoid conflicts

### AST Implementation Guide (Future)

When ready to add Abstract Syntax Tree construction:

1. **Create node classes** in `parser/ast_nodes.py`:
```python
class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self):
        self.statements = []

class BinaryOpNode(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
```

2. **Modify parser methods** to return nodes:
```python
def parse_expression(self):
    # Instead of just validating...
    if token_type == TokenType.SUM_OF:
        self.advance()
        left = self.parse_expression()
        self.expect(TokenType.AN)
        right = self.parse_expression()
        return BinaryOpNode('SUM_OF', left, right)  # Return AST node
```

3. **Use AST for interpretation** - traverse tree and execute nodes

The current parser structure makes this transition straightforward!

## Dependencies

- Python 3.x
- tkinter (usually included with Python)
- No external packages required

## Contributing

This is an academic project for CMSC 124. The implementation follows course requirements and LOLCode specifications.

## License

Educational use for CMSC 124 coursework at the University of the Philippines Los Baños.