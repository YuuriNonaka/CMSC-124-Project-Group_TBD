import re
import sys

try:
    from .lol_tokens import TokenType, COMPILED_PATTERNS
except ImportError:
    from lol_tokens import TokenType, COMPILED_PATTERNS


def remove_comments(line):
    #find btw keyword (case insensitive, word boundary)
    btw_pattern = re.compile(r'\bBTW\b', re.IGNORECASE)
    match = btw_pattern.search(line)
    
    if match:
        #keep everything before the BTW
        return line[:match.start()].rstrip()
    return line

def classify_identifier(prev_tokens):
    
    if not prev_tokens:
        return TokenType.VARIDENT
    
    #check the last token
    last_token = prev_tokens[-1][1]
    
    #function definition
    if last_token == TokenType.HOW_IZ_I:
        return TokenType.FUNCIDENT
    
    #function call
    if last_token == TokenType.I_IZ:
        return TokenType.FUNCIDENT
    
    #loop label start
    if last_token == TokenType.IM_IN_YR:
        return TokenType.LABEL
    
    #loop label end
    if last_token == TokenType.IM_OUTTA_YR:
        return TokenType.LABEL
    
    #defaul
    return TokenType.VARIDENT


def tokenize_line(line, line_num, all_tokens_so_far=None):
    #tokenize one line at a time
    if all_tokens_so_far is None:
        all_tokens_so_far = []

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
        #skip spaces
        if line[pos].isspace():
            pos += 1
            continue
        
        #try matching with our patterns
        matched = False
        for pattern, token_type in COMPILED_PATTERNS:
            match = pattern.match(line, pos)
            if match:
                lexeme = match.group(0)

                #if regular identifier then figure out what kind it is
                if token_type == TokenType.VARIDENT:
                    context_tokens = all_tokens_so_far + tokens
                    token_type = classify_identifier(context_tokens)
                
                tokens.append((lexeme, token_type, line_num))
                pos = match.end()
                matched = True
                break
        
        if not matched:
            #cant match this token then just grab as unknown
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

        #tokenize this line
        line_tokens = tokenize_line(line, line_num, tokens)
        
        #add tokens and a linebreak
        if line_tokens:
            tokens.extend(line_tokens)
            #add linebreak after each line
            tokens.append(('\\n', TokenType.LINEBREAK, line_num))

        line_num += 1

    #remove the last linebreak if theres one
    if tokens and tokens[-1][1] == TokenType.LINEBREAK:
        tokens.pop()
    
    return tokens


def print_tokens_table(tokens, show_linebreaks=False):
    #print the tokens
    if not tokens:
        print("No tokens found.")
        return
    
    #hide linebreaks
    display_tokens = tokens if show_linebreaks else [t for t in tokens if t[1] != TokenType.LINEBREAK]
    
    if not display_tokens:
        print("No tokens found.")
        return
    
    #column widths
    max_lexeme = max(len(str(t[0])) for t in display_tokens)
    max_type = max(len(str(t[1].value)) for t in display_tokens)
    max_lexeme = max(max_lexeme, len("Lexeme"))
    max_type = max(max_type, len("Classification"))
    
    #print the header
    print("\n" + "="*80)
    print(f"{'Lexeme':<{max_lexeme}}  {'Classification':<{max_type}}  Line")
    print("="*80)
    
    #print each token
    for lexeme, token_type, line_num in display_tokens:
        print(f"{lexeme:<{max_lexeme}}  {token_type.value:<{max_type}}  {line_num}")
    
    print("="*80)
    print(f"Total tokens: {len(display_tokens)}")
    if not show_linebreaks:
        linebreak_count = len(tokens) - len(display_tokens)
        if linebreak_count > 0:
            print(f"(Linebreak tokens hidden: {linebreak_count})")
    print()


def analyze_file(filename, show_linebreaks=False):
    #read and analyze the lolcode file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        print(f"\n{'='*80}")
        print(f"Analyzing file: {filename}")
        print(f"{'='*80}")
        
        tokens = tokenize_program(source_code)
        print_tokens_table(tokens, show_linebreaks)
        
        return tokens
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    filename = sys.argv[1]
    show_linebreaks = '--show-linebreaks' in sys.argv
    
    if not filename.endswith('.lol'):
        print("Error reading file (only .lol files)")
    
    analyze_file(filename, show_linebreaks)