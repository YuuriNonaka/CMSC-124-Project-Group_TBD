# LOLCode Interpreter

A comprehensive interpreter for the LOLCode esoteric programming language, developed as a project for CMSC 124 (Design and Implementation of Programming Languages) at the University of the Philippines Los Baños.

## Project Overview

This interpreter implements lexical, syntactical, and semantic analysis for LOLCode programs (.lol files). The project follows the specifications outlined in the CMSC 124 project requirements and aims to create a fully functional interpreter with a graphical user interface.

### Current Status: **Lexical Analysis Complete + GUI Implemented** ✔

The lexer is fully implemented and can tokenize LOLCode programs according to the language specifications. A graphical user interface has been added for easier interaction with the interpreter.

## Project Structure

```
lolcode_interpreter/
├── lexer/
│   ├── __init__.py        # Package initializer - exports tokenize_program and TokenType
│   ├── lexer.py           # Main lexical analyzer
│   └── lol_tokens.py      # Token definitions, patterns, and human-readable descriptions
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

### Running the CLI Lexer
```bash
python lexer/lexer.py test_cases/01_variables.lol [--show-linebreaks]
```

## GUI Features

The graphical interface provides an integrated development environment for LOLCode:

### Functional Features ✅
- **Text Editor Panel** - Edit LOLCode source code with syntax support
- **File Operations** - Open, Save, and Save As functionality with keyboard shortcuts
- **Lexemes Table** - View tokenized output with human-readable classifications
- **File Path Display** - Shows currently loaded file
- **Execute Button** - Run lexical analysis on the current code

### Token Display Format
The lexemes table displays tokens with descriptive classifications:
- `HAI` → "Code Delimiter" (not "HAI")
- `I HAS A` → "Variable Declaration" (not "I_HAS_A")
- `VISIBLE` → "Output Keyword" (not "VISIBLE")
- `12` → "Integer Literal" (not "NUMBR Literal")

### Placeholder Features (Coming Soon) 🔲
- **Symbol Table** - Will display variable declarations and values
- **Console Output** - Will show program execution results and I/O

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
  - `create_symbol_table()` - Placeholder for future symbol table implementation
  - `execute()` - Runs lexical analysis and updates the lexemes table
  - `open_file()` / `save_file()` / `save_file_as()` - File operations

**GUI Layout:**
```
┌───────────────────────────────────────────────────┐
│ File Menu                                         │
├───────────────────────────────────────────────────┤
│ File Path: (None)                                 │
├───────────────┬──────────────────┬─────────────────┤
│               │    Lexemes       │  SYMBOL TABLE   │
│               ├──────────────────┤                 │
│               │ Lexeme | Class   │  Identifier|Value│
│  Text Editor  │ ──────────────── │  ─────────────── │
│               │  HAI   | Code    │  (placeholder)  │
│               │        | Delimiter│                 │
│               │  ...   | ...     │                 │
│               │                  │                 │
├───────────────┴──────────────────┴─────────────────┤
│                  [ EXECUTE ]                       │
├───────────────────────────────────────────────────┤
│ Console Output (placeholder)                       │
│                                                    │
└───────────────────────────────────────────────────┘
```

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

### GUI Integration

The GUI integrates with the lexer by:
1. Adding the `lexer/` directory to Python's module search path
2. Importing `tokenize_program()` function and `TOKEN_DESCRIPTIONS` dictionary
3. Passing editor content to the tokenizer
4. Displaying results in a formatted table with human-readable classifications
5. Filtering out LINEBREAK tokens for cleaner display

## Testing

Test cases are organized in the `test_cases/` directory, covering:
- Variable declarations and initialization
- User input (GIMMEH)
- Arithmetic operations
- Boolean operations
- Control flow structures
- Functions
- Edge cases and error conditions

**To test with GUI:**
1. Launch `python lolcode_gui.py`
2. Open a test file from `test_cases/`
3. Click EXECUTE
4. View tokens in the Lexemes table with descriptive classifications

**To test with CLI:**
```bash
python lexer/lexer.py test_cases/01_variables.lol
```

## Next Steps

### Phase 2: Syntax Analysis (Parser) - IN PROGRESS
- Implement grammar rules for LOLCode
- Build Abstract Syntax Tree (AST)
- Validate program structure
- Integrate with GUI

### Phase 3: Semantic Analysis
- Type checking and inference
- Variable scope management
- Expression evaluation
- Runtime error detection

### Phase 4: Complete GUI Implementation
- ✅ File explorer for loading .lol files (DONE)
- ✅ Text editor for code viewing/editing (DONE)
- ✅ Token list display with human-readable descriptions (DONE)
- ⬜ Symbol table display (parser required)
- ⬜ Console for I/O (interpreter required)
- ⬜ Execute/Run functionality (interpreter required)

## Project Requirements

- **Prohibited**: No use of Flex/Lex, YACC/Bison, PEG, or any parser generator tools
- **Required**: Custom implementation of lexical and syntax analyzers
- **Evaluation**: Three progress presentations (lexer, parser, semantics)
- **Minimum**: Interpreter must evaluate at least one operation/statement

## Development Guidelines

When continuing work on this codebase:

1. **Lexer is complete** - Focus on parser/semantic analysis next
2. **GUI framework ready** - Add parser and interpreter integration
3. **Follow the pattern ordering** in `lol_tokens.py` - order matters!
4. **Context is key** - The `classify_identifier` function shows how to use previous tokens for disambiguation
5. **Test incrementally** - Use the test cases to verify each feature
6. **Maintain token structure** - (lexeme, TokenType, line_number) tuples throughout
7. **Refer to specifications** - The project specs PDF contains authoritative language rules
8. **Display layer separation** - `TokenType` enum values are for internal use; `TOKEN_DESCRIPTIONS` provides user-friendly names for the GUI

### Common Issues to Watch

- Multi-word keywords must be matched before their single-word components
- NOOB appears in both literals and type keywords - pattern order handles this
- Identifiers need contextual classification based on preceding tokens
- Linebreak tokens are added but can be hidden in output
- GUI imports require the lexer directory to be in Python's path
- Token descriptions are purely for display - the internal TokenType enum remains unchanged

## Dependencies

- Python 3.x
- tkinter (usually included with Python)
- No external packages required