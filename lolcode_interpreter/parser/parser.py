from lexer.lol_tokens import TokenType


class SyntaxError(Exception): #custom error handling with line number tracking
    pass

class Parser: #uses recursive descent
    
    def __init__(self, tokens): #initializes parser with the token list in lol_tokens
        #filters out linebreaks for easier parsing
        self.tokens = [t for t in tokens if t[1] != TokenType.LINEBREAK]
        self.pos = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def peek(self, offset=0):
        #preview future tokens without advancing position for grammar decisions based on upcoming tokens
        #i.e., check if next token is 'else' after 'if', or look for operators after identifiers
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def advance(self):
        #goes to the next token
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return self.current_token
    
    def expect(self, token_type, error_msg=None):
        #checks if current token matches expected type, then return it and move to next token
        if not self.current_token:
            raise SyntaxError(f"Unexpected end of file. Expected {token_type.value}")
        
        if self.current_token[1] != token_type:
            line_num = self.current_token[2]
            if error_msg:
                raise SyntaxError(f"{error_msg} on line {line_num}")
            else:
                raise SyntaxError(
                    f"Expected {token_type.value} but got '{self.current_token[0]}' "
                    f"on line {line_num}"
                )
        token = self.current_token #stores current token before moving forward
        self.advance() #advances to the next token in the stream
        return token
    
    def match(self, *token_types):
        #checks if current token matches any of the given token types
        if not self.current_token:
            return False
        return self.current_token[1] in token_types

    def parse(self):
        #main parsing entry point, validates entire program structure from tokens
        if not self.tokens:
            raise SyntaxError("Empty program. LOLCode programs must start with HAI.")
        
        self.parse_program()
        
        #ensures no extra tokens remain after the program ends
        if self.current_token:
            line_num = self.current_token[2]
            raise SyntaxError(
                f"Unexpected code after KTHXBYE on line {line_num}. "
                f"Program must end with KTHXBYE."
            )

    def parse_program(self):
        #parses required program structure: HAI [version] [body] KTHXBYE
        self.expect(TokenType.HAI, "Program must start with HAI")
        
        #optional version number after HAI (may be omitted)
        if self.match(TokenType.NUMBAR):
            self.advance()  #moves past version number
        
        #parses the main body content
        self.parse_main_body()
        
        #program must end with KTHXBYE
        self.expect(TokenType.KTHXBYE, "Program must end with KTHXBYE")

    def parse_main_body(self):
        #optional variable declarations using wazzup, followed by statements
        if self.match(TokenType.WAZZUP):
            self.parse_wazzup_block()
        
        #parses all statements until we reach KTHXBYE
        while self.current_token and not self.match(TokenType.KTHXBYE):
            self.parse_statement()

    def parse_wazzup_block(self):
        #parses variable declaration block: WAZZUP [declarations] BUHBYE
        self.expect(TokenType.WAZZUP)
        
        #parses all variable declarations until BUHBYE marker
        while self.current_token and not self.match(TokenType.BUHBYE):
            if self.match(TokenType.I_HAS_A):
                self.parse_variable_declaration()
            else:
                line_num = self.current_token[2]
                raise SyntaxError(
                    f"Expected variable declaration (I HAS A) or BUHBYE in WAZZUP block, "
                    f"but got '{self.current_token[0]}' on line {line_num}"
                )
        
        self.expect(TokenType.BUHBYE, "WAZZUP block must end with BUHBYE")

    def parse_variable_declaration(self):
        #parses variable declarations: I HAS A <variable> [ITZ <initial value>]
        self.expect(TokenType.I_HAS_A)
        
        #requires a variable identifier after I HAS A
        if not self.match(TokenType.VARIDENT):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(
                f"Expected variable identifier after 'I HAS A' on line {line_num}"
            )
        
        self.advance()  #move past variable name
        
        #optional initialization with ITZ keyword
        if self.match(TokenType.ITZ):
            self.advance()  # Move past ITZ
            self.parse_expression()
    