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