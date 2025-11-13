# LOLCode Interpreter

A comprehensive interpreter for the LOLCode esoteric programming language, developed as a project for CMSC 124 (Design and Implementation of Programming Languages) at the University of the Philippines Los Baños.

## Project Overview

This interpreter implements lexical, syntactical, and semantic analysis for LOLCode programs (.lol files). The project follows the specifications outlined in the CMSC 124 project requirements and aims to create a fully functional interpreter with a graphical user interface.

### Current Status: **Abstract Syntax Tree Complete** ✔

- **Lexer**: Fully implemented and operational ✅
- **Parser**: Complete syntax validation with AST construction ✅
- **AST**: Complete node structure for all LOLCode constructs ✅
- **Semantic Analyzer**: Basic symbol table construction implemented ⚙️
- **GUI**: Integrated interface with all phases ✅

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

**Parser with AST:**
```python
from lexer import tokenize_program
from parser import Parser, SyntaxError as LOLSyntaxError

code = open('test_cases/01_variables.lol').read()
tokens = tokenize_program(code)

try:
    parser = Parser(tokens)
    ast = parser.parse()  # Returns AST root node
    print("✅ Syntax is valid!")
    print(f"Program has {len(ast.statements)} statements")
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
- **Syntax Validation** - Real-time syntax checking with detailed error messages and AST construction
- **Console Output** - Displays analysis results, syntax errors, and execution status
- **File Path Display** - Shows currently loaded file

### Analysis Pipeline
When you click **EXECUTE**, the interpreter runs:
1. **Lexical Analysis** → Tokenizes the source code
2. **Syntax Analysis** → Validates program structure and builds AST
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

### `parser/ast_nodes.py`
Defines AST node classes for representing LOLCode program structure.

**Base Class:**
- **ASTNode**: Base class for all AST nodes

**Program Structure:**
- **ProgramNode**: Root node representing entire program
  - `version` - Optional version number
  - `statements` - List of statement nodes

**Variable Operations:**
- **VariableDeclNode**: Variable declaration (`I HAS A`)
  - `var_name` - Variable identifier
  - `initial_value` - Optional initialization expression
- **AssignmentNode**: Variable assignment (`R`)
  - `var_name` - Target variable
  - `expression` - Value expression

**I/O Operations:**
- **VisibleNode**: Output statement
  - `expressions` - List of expressions to display
- **GimmehNode**: Input statement
  - `var_name` - Variable to receive input

**Expressions:**
- **LiteralNode**: Literal values (numbers, strings, booleans)
  - `value` - Literal value
  - `literal_type` - Token type
- **VariableNode**: Variable reference
  - `var_name` - Referenced variable
- **BinaryOpNode**: Binary operations (arithmetic, boolean)
  - `operator` - Operation type
  - `left`, `right` - Operand expressions
- **UnaryOpNode**: Unary operations (NOT)
  - `operator` - Operation type
  - `operand` - Single operand
- **InfiniteArityOpNode**: Variable-arity operations (ALL OF, ANY OF, SMOOSH)
  - `operator` - Operation type
  - `operands` - List of operand expressions
- **ComparisonNode**: Comparison operations
  - `operator` - Comparison type
  - `left`, `right` - Operands
- **TypecastNode**: Type conversion
  - `expression` - Expression to cast
  - `target_type` - Desired type

**Control Flow:**
- **ConditionalNode**: If-else structure (O RLY?)
  - `if_block` - Statements for true condition
  - `elif_blocks` - List of else-if clauses
  - `else_block` - Statements for false condition
- **ElifClauseNode**: Else-if clause (MEBBE)
  - `condition` - Condition expression
  - `statements` - Block statements
- **SwitchNode**: Switch-case structure (WTF?)
  - `cases` - List of case nodes
  - `default_case` - Default case statements
- **CaseNode**: Single case (OMG)
  - `literal_value` - Case value
  - `statements` - Block statements
- **LoopNode**: Loop structure (IM IN YR)
  - `label` - Loop identifier
  - `operation` - UPPIN or NERFIN
  - `var_name` - Loop variable
  - `condition` - Optional loop condition
  - `condition_type` - TIL or WILE
  - `statements` - Loop body

**Functions:**
- **FunctionDefNode**: Function definition (HOW IZ I)
  - `func_name` - Function identifier
  - `parameters` - List of parameter names
  - `statements` - Function body
- **FunctionCallNode**: Function call (I IZ)
  - `func_name` - Function identifier
  - `arguments` - List of argument expressions
- **ReturnNode**: Return statement (FOUND YR)
  - `expression` - Return value
- **BreakNode**: Break statement (GTFO)

### `parser/parser.py`
Implements recursive-descent syntax validation and AST construction for LOLCode programs.

**Key Components:**
- **Parser Class**: Main parsing engine with token stream management
  - `parse()` - Entry point for full program validation, returns AST
  - `parse_program()` - Validates HAI...KTHXBYE structure, returns ProgramNode
  - `parse_main_body()` - Handles optional WAZZUP block and statements
  - `parse_statement()` - Dispatches to specific statement parsers, returns statement nodes
  - `parse_expression()` - Validates expressions with proper operator syntax, returns expression nodes
  - Control flow parsers: `parse_conditional()`, `parse_switch()`, `parse_loop()` - return control flow nodes
  - Function parsers: `parse_function_definition()`, `parse_function_call()` - return function nodes

**Custom Exception:**
- **SyntaxError**: Custom exception with line number tracking for detailed error reporting

**AST Construction Features:**
- Complete tree structure representing program semantics
- All statement types create corresponding AST nodes
- Expression parsing builds nested expression trees
- Control flow structures maintain block hierarchies
- Functions preserve parameter and argument lists

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
- AST-based semantic analysis
- Type inference and validation
- Scope management
- Full expression evaluation

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

### Syntax Analysis & AST Construction Details

1. **Recursive-Descent Parsing**: The parser uses recursive-descent techniques without any parser generators, as required by project specifications.

2. **AST Construction**: Each parsing method constructs and returns appropriate AST nodes:
   - Terminal nodes (literals, variables) are leaf nodes
   - Operators create nodes with child expressions
   - Statements create nodes with nested statement lists
   - The entire program is represented as a tree structure

3. **Token Stream Management**:
   - Linebreak tokens are filtered out for cleaner parsing
   - Current position tracked with lookahead capability
   - Token consumption with type validation

4. **Error Reporting**:
   - All syntax errors include specific line numbers
   - Clear messages indicate what was expected vs. what was found
   - Examples: "Expected variable identifier after 'I HAS A' on line 12"

5. **Expression Parsing**:
   - Validates operator arity (binary operators require exactly 2 operands)
   - Ensures proper use of `AN` separator between operands
   - Checks for `MKAY` terminators in infinite arity operations
   - Handles nested expressions recursively
   - Builds expression trees for evaluation

6. **Control Flow Validation**:
   - Ensures proper block structure (O RLY...OIC, WTF...OIC)
   - Validates loop label matching
   - Checks required clauses (YA RLY after O RLY?)
   - Maintains block hierarchies in AST nodes

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
   - Token-based analysis (will migrate to AST-based)
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
5. Running complete pipeline: Lexer → Parser (with AST) → Semantics
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
5. Check console for syntax validation results and AST construction

### Testing Individual Components

**Lexer (CLI):**
```bash
python lexer/lexer.py test_cases/01_variables.lol
```

**Parser with AST (Python):**
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
    ast = parser.parse()  # Returns ProgramNode
    print("✅ Syntax is valid!")
    print(f"Program version: {ast.version}")
    print(f"Number of statements: {len(ast.statements)}")
    
    # Examine first statement
    first_stmt = ast.statements[0]
    print(f"First statement type: {type(first_stmt).__name__}")
    
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
- ⬜ Migration to AST-based semantic analysis
- ⬜ Assignment statement handling (`<var> R <value>`)
- ⬜ Type checking and inference
- ⬜ Variable scope management
- ⬜ Full expression evaluation
- ⬜ Runtime error detection

### Phase 4: AST-Based Interpreter - NEXT
- ✅ AST node classes complete
- ✅ Parser constructs AST during validation
- ⬜ AST traversal and evaluation
- ⬜ Expression evaluation with type coercion
- ⬜ Control flow execution (conditionals, loops)
- ⬜ Function call execution
- ⬜ I/O operations (VISIBLE, GIMMEH)

### Phase 5: Complete Interpreter Implementation
- ⬜ Runtime environment with variable storage
- ⬜ Type system and automatic conversions
- ⬜ Function call stack management
- ⬜ Loop and control flow execution
- ⬜ Error handling and runtime validation
- ⬜ Connect to GUI console for interactive I/O

### Phase 6: Final GUI Integration
- ✅ File explorer for loading .lol files
- ✅ Text editor for code viewing/editing
- ✅ Token list display with human-readable descriptions
- ✅ Symbol table display
- ✅ Console output for errors and messages
- ⬜ Interactive console for GIMMEH input during execution
- ⬜ Step-by-step execution debugging
- ⬜ AST visualization (optional)

## Project Requirements

- **Prohibited**: No use of Flex/Lex, YACC/Bison, PEG, or any parser generator tools ✅
- **Required**: Custom implementation of lexical and syntax analyzers ✅
- **Evaluation**: Three progress presentations (lexer ✅, parser ✅, semantics ⚙️)
- **Minimum**: Interpreter must evaluate at least one operation/statement

## Development Guidelines

When continuing work on this codebase:

1. **Lexer is complete** ✅ - Fully functional and tested
2. **Parser is complete** ✅ - Validates all LOLCode syntax and builds AST
3. **AST is complete** ✅ - All node types defined and constructed
4. **Semantic module started** 📄 - Symbol table construction implemented (needs AST migration)
5. **GUI framework ready** - All phases integrated with console output
6. **Follow the pattern ordering** in `lol_tokens.py` - order matters!
7. **Context is key** - The `classify_identifier` function shows how to use previous tokens
8. **Test incrementally** - Use test cases to verify each feature
9. **Maintain token structure** - (lexeme, TokenType, line_number) tuples throughout
10. **Refer to specifications** - The project specs PDF contains authoritative rules
11. **Display layer separation** - `TokenType` for internal use; `TOKEN_DESCRIPTIONS` for GUI
12. **Module organization** - Keep lexer, parser, and semantics in separate packages
13. **Error handling** - Always provide line numbers and clear messages
14. **AST structure** - Tree represents program semantics, ready for interpretation

### Common Issues to Watch

- Multi-word keywords must be matched before single-word components
- NOOB appears in both literals and type keywords - pattern order handles this
- Identifiers need contextual classification based on preceding tokens
- Linebreak tokens are added but filtered in parser
- GUI imports require project root in Python's path
- Token descriptions are purely for display - internal TokenType unchanged
- Import paths relative to project root (e.g., `from parser import Parser`)
- Custom SyntaxError imported as `LOLSyntaxError` to avoid conflicts
- AST nodes should be traversed, not tokens, for semantic analysis

### AST Traversal Guide (For Interpreter Implementation)

When implementing the interpreter using the AST:

1. **Start with the root** (ProgramNode):
```python
def execute_program(ast):
    for statement in ast.statements:
        execute_statement(statement)
```

2. **Dispatch based on node type**:
```python
def execute_statement(node):
    if isinstance(node, VariableDeclNode):
        handle_declaration(node)
    elif isinstance(node, AssignmentNode):
        handle_assignment(node)
    elif isinstance(node, VisibleNode):
        handle_output(node)
    # ... etc
```

3. **Evaluate expressions recursively**:
```python
def evaluate_expression(node, symbol_table):
    if isinstance(node, LiteralNode):
        return convert_literal(node.value, node.literal_type)
    elif isinstance(node, VariableNode):
        return symbol_table.get(node.var_name, "NOOB")
    elif isinstance(node, BinaryOpNode):
        left = evaluate_expression(node.left, symbol_table)
        right = evaluate_expression(node.right, symbol_table)
        return apply_binary_op(node.operator, left, right)
    elif isinstance(node, UnaryOpNode):
        operand = evaluate_expression(node.operand, symbol_table)
        return apply_unary_op(node.operator, operand)
    # ... etc
```

4. **Handle control flow**:
```python
def execute_conditional(node, symbol_table):
    # Evaluate IT variable for condition
    condition = symbol_table.get('IT', "NOOB")
    
    if is_truthy(condition):
        for stmt in node.if_block:
            execute_statement(stmt, symbol_table)
    else:
        # Check elif blocks
        for elif_clause in node.elif_blocks:
            elif_condition = evaluate_expression(elif_clause.condition, symbol_table)
            if is_truthy(elif_condition):
                for stmt in elif_clause.statements:
                    execute_statement(stmt, symbol_table)
                return
        # Execute else block
        for stmt in node.else_block:
            execute_statement(stmt, symbol_table)
```

5. **Maintain runtime state**:
```python
class RuntimeEnvironment:
    def __init__(self):
        self.symbol_table = {'IT': 'NOOB'}
        self.functions = {}
        self.call_stack = []
    
    def declare_variable(self, name, value="NOOB"):
        self.symbol_table[name] = value
    
    def get_variable(self, name):
        return self.symbol_table.get(name, "NOOB")
    
    def set_variable(self, name, value):
        self.symbol_table[name] = value
```

## AST Node Reference

### Quick Node Type Guide

**Program Structure:**
- `ProgramNode` - Root of entire program

**Statements:**
- `VariableDeclNode` - Variable declarations
- `AssignmentNode` - Variable assignments
- `VisibleNode` - Output statements
- `GimmehNode` - Input statements
- `ConditionalNode` - If-else structures
- `SwitchNode` - Switch-case structures
- `LoopNode` - Loop structures
- `FunctionDefNode` - Function definitions
- `FunctionCallNode` - Function calls
- `ReturnNode` - Return statements
- `BreakNode` - Break statements

**Expressions:**
- `LiteralNode` - Literal values
- `VariableNode` - Variable references
- `BinaryOpNode` - Binary operations
- `UnaryOpNode` - Unary operations
- `InfiniteArityOpNode` - Multi-operand operations
- `ComparisonNode` - Comparison operations
- `TypecastNode` - Type conversions

**Supporting Nodes:**
- `ElifClauseNode` - Else-if clauses
- `CaseNode` - Switch cases

## Dependencies

- Python 3.x
- tkinter (usually included with Python)
- No external packages required

## Future Enhancements

**Interpreter Phase:**
- Runtime environment with proper variable scoping
- Type system with automatic conversions
- Function call stack with local scopes
- Full control flow execution
- I/O handling with user interaction

**GUI Improvements:**
- Syntax highlighting in text editor
- AST tree visualization
- Step-by-step execution debugger
- Breakpoint support
- Variable watch window

**Advanced Features:**
- Error recovery during parsing
- Better error messages with suggestions
- Code formatting/beautification
- LOLCode-to-Python transpiler
- Performance optimizations
