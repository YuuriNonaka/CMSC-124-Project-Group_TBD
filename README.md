# LOLCode Interpreter

A comprehensive interpreter for the LOLCode esoteric programming language, developed as a project for CMSC 124 (Design and Implementation of Programming Languages) at the University of the Philippines Los Baños.

## Project Overview

This interpreter implements lexical, syntactical, and semantic analysis for LOLCode programs (.lol files). The project follows the specifications outlined in the CMSC 124 project requirements and aims to create a fully functional interpreter with a graphical user interface.

### Current Status: **Lexical Analysis Complete** ✓

The lexer is fully implemented and can tokenize LOLCode programs according to the language specifications.

## Project Structure

```
lolcode_interpreter/
├── lexer/
│   ├── lexer.py           # Main lexical analyzer
│   └── lol_tokens.py      # Token definitions and patterns
├── test_cases/
│   ├── 01_variables.lol   # Test: Variable declarations
│   ├── 02_gimmeh.lol      # Test: User input
│   └── ...                # Additional test files
├── .gitignore
└── README.md
```

## File Descriptions

### `lexer/lol_tokens.py`
Defines the token types and regular expression patterns for LOLCode lexemes.

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

**Usage:**
```bash
python lexer.py <filename.lol> [--show-linebreaks]
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

## Testing

Test cases are organized in the `test_cases/` directory, covering:
- Variable declarations and initialization
- User input (GIMMEH)
- Arithmetic operations
- Boolean operations
- Control flow structures
- Functions
- Edge cases and error conditions

## Next Steps

### Phase 2: Syntax Analysis (Parser)
- Implement grammar rules for LOLCode
- Build Abstract Syntax Tree (AST)
- Validate program structure

### Phase 3: Semantic Analysis
- Type checking and inference
- Variable scope management
- Expression evaluation
- Runtime error detection

### Phase 4: GUI Implementation
- File explorer for loading .lol files
- Text editor for code viewing/editing
- Token list display
- Symbol table display
- Console for I/O
- Execute/Run functionality

## Project Requirements

- **Prohibited**: No use of Flex/Lex, YACC/Bison, PEG, or any parser generator tools
- **Required**: Custom implementation of lexical and syntax analyzers
- **Evaluation**: Three progress presentations (lexer, parser, semantics)
- **Minimum**: Interpreter must evaluate at least one operation/statement

## Development Guidelines

When continuing work on this codebase:

1. **Lexer is complete** - Focus on parser/semantic analysis next
2. **Follow the pattern ordering** in `lol_tokens.py` - order matters!
3. **Context is key** - The `classify_identifier` function shows how to use previous tokens for disambiguation
4. **Test incrementally** - Use the test cases to verify each feature
5. **Maintain token structure** - (lexeme, TokenType, line_number) tuples throughout
6. **Refer to specifications** - The project specs PDF contains authoritative language rules

### Common Issues to Watch

- Multi-word keywords must be matched before their single-word components
- NOOB appears in both literals and type keywords - pattern order handles this
- Identifiers need contextual classification based on preceding tokens
- Linebreak tokens are added but can be hidden in output

## License

Academic project for CMSC 124, UP Los Baños

## Contact

Institute of Computer Science  
College of Arts and Sciences  
University of the Philippines Los Baños