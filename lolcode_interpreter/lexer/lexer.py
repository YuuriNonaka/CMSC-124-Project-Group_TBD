import re
import sys
from lol_tokens import TokenType, COMPILED_PATTERNS


def remove_comments(line):
    #find btw keyword (case insensitive, word boundary)
    btw_pattern = re.compile(r'\bBTW\b', re.IGNORECASE)
    match = btw_pattern.search(line)
    
    if match:
        #preserve everything before btw
        return line[:match.start()].rstrip()
    return line


def tokenize_line(line, line_num):
    tokens = []
    line = line.strip()
    
    if not line:
        return tokens
    
    #remove inline comments first
    line = remove_comments(line)
    
    if not line:
        return tokens
    
    pos = 0
    while pos < len(line):
        #skip whitespace
        if line[pos].isspace():
            pos += 1
            continue
        
        #try to match against each pattern
        matched = False
        for pattern, token_type in COMPILED_PATTERNS:
            match = pattern.match(line, pos)
            if match:
                lexeme = match.group(0)
                tokens.append((lexeme, token_type, line_num))
                pos = match.end()
                matched = True
                break
        
        if not matched:
            #unknown token - grab the next non-whitespace sequence
            end_pos = pos + 1
            while end_pos < len(line) and not line[end_pos].isspace():
                end_pos += 1
            lexeme = line[pos:end_pos]
            tokens.append((lexeme, TokenType.UNKNOWN, line_num))
            pos = end_pos
    
    return tokens


def tokenize_program(source_code):
    lines = source_code.split('\n')
    tokens = []
    line_num = 1
    in_multiline_comment = False
    
    for line in lines:
        stripped = line.strip()
        
        #check for multiline comment start
        if re.match(r'\bOBTW\b', stripped, re.IGNORECASE):
            in_multiline_comment = True
            line_num += 1
            continue
        
        #check for multiline comment end
        if re.match(r'\bTLDR\b', stripped, re.IGNORECASE):
            in_multiline_comment = False
            line_num += 1
            continue
        
        #skip lines inside multiline comments
        if in_multiline_comment:
            line_num += 1
            continue
        
        #tokenize the line
        line_tokens = tokenize_line(line, line_num)
        tokens.extend(line_tokens)
        line_num += 1
    
    return tokens


def print_tokens_table(tokens):
    if not tokens:
        print("No tokens found.")
        return
    
    #calculate column widths
    max_lexeme = max(len(str(t[0])) for t in tokens)
    max_type = max(len(str(t[1].value)) for t in tokens)
    max_lexeme = max(max_lexeme, len("Lexeme"))
    max_type = max(max_type, len("Classification"))
    
    #print header
    print("\n" + "="*80)
    print(f"{'Lexeme':<{max_lexeme}}  {'Classification':<{max_type}}  Line")
    print("="*80)
    
    #print tokens
    for lexeme, token_type, line_num in tokens:
        print(f"{lexeme:<{max_lexeme}}  {token_type.value:<{max_type}}  {line_num}")
    
    print("="*80)
    print(f"Total tokens: {len(tokens)}\n")


def analyze_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        print(f"\n{'='*80}")
        print(f"Analyzing file: {filename}")
        print(f"{'='*80}")
        
        tokens = tokenize_program(source_code)
        print_tokens_table(tokens)
        
        return tokens
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

if len(sys.argv) != 2:
    print("Usage: python lexer.py <filename.lol>")
    sys.exit(1)

filename = sys.argv[1]

if not filename.endswith('.lol'):
    print("Warning: File does not have .lol extension")

analyze_file(filename)
