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
        #checks if current token matches expected type, then return it andmoves to next token
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
            self.advance()  #moves past ITZ
            self.parse_expression()

    def parse_statement(self):
        #parses one statement: output, input, assignment, conditionals, loops, functions, etc.
        #has separate functions for each type
        if not self.current_token:
            return
        
        token_type = self.current_token[1]
        line_num = self.current_token[2]
        
        #VISIBLE - output statement
        if token_type == TokenType.VISIBLE:
            self.parse_visible_statement()
        
        #GIMMEH - input statement  
        elif token_type == TokenType.GIMMEH:
            self.parse_gimmeh_statement()
        
        #Assignment: <variable> R <expression>
        elif token_type == TokenType.VARIDENT:
            self.parse_assignment_or_expression()
        
        #O RLY? - if/else conditional
        elif token_type == TokenType.O_RLY:
            self.parse_conditional()
        
        #WTF? - switch/case statement
        elif token_type == TokenType.WTF:
            self.parse_switch()
        
        #IM IN YR - loop construct
        elif token_type == TokenType.IM_IN_YR:
            self.parse_loop()
        
        #HOW IZ I - function definition
        elif token_type == TokenType.HOW_IZ_I:
            self.parse_function_definition()
        
        #I IZ - function call
        elif token_type == TokenType.I_IZ:
            self.parse_function_call()
        
        #FOUND YR - return from function
        elif token_type == TokenType.FOUND_YR:
            self.parse_return_statement()
        
        #GTFO - break out of loop or switch
        elif token_type == TokenType.GTFO:
            self.advance()  #moves past GTFO token
        
        #expression that evaluates to IT variable
        elif self.is_expression_start():
            self.parse_expression()
        
        else:
            raise SyntaxError(
                f"Unexpected statement starting with '{self.current_token[0]}' "
                f"on line {line_num}"
            )

    def parse_visible_statement(self):
        #parses VISIBLE statement: output one or more expressions separated by spaces
        self.expect(TokenType.VISIBLE)
        
        #requires at least one expression
        if not self.is_expression_start():
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"VISIBLE requires at least one expression on line {line_num}")
        
        #parses first expression
        self.parse_expression()
        
        #parses additional expressions on the same line (space-separated)
        while self.current_token and self.is_expression_start() and self.current_token[1] != TokenType.NEWLINE:
            self.parse_expression()
        
        #consumes the newline at the end of the statement if present
        if self.current_token and self.current_token[1] == TokenType.NEWLINE:
            self.advance()

    def parse_gimmeh_statement(self):
        #parses GIMMEH statement: read input into a variable
        self.expect(TokenType.GIMMEH)
        self.expect(TokenType.VARIDENT, "GIMMEH requires a variable identifier")

    def parse_assignment_or_expression(self):
        #parses either variable assignment (<var> R <expr>) or variable reference as expression
        var_token = self.current_token
        self.advance()  #moves past variable name
        
        if self.match(TokenType.R):
            #this is an assignment: variable R expression
            self.advance()  #moves past R token
            self.parse_expression()
        #if no R token, this is just a variable reference (valid as standalone expression)

    def parse_conditional(self):
        #parses if/else conditional: O RLY? → YA RLY [MEBBE] [NO WAI] → OIC
        self.expect(TokenType.O_RLY)
        
        #requires if block
        self.expect(TokenType.YA_RLY, "O RLY? must be followed by YA RLY")
        
        #parses statements until MEBBE (else if), NO WAI (else), or OIC (end)
        while self.current_token and not self.match(TokenType.MEBBE, TokenType.NO_WAI, TokenType.OIC):
            self.parse_statement()
        
        #parse any else-if (MEBBE) blocks
        while self.match(TokenType.MEBBE):
            self.advance()  #moves MEBBE
            self.parse_expression()  #parse the condition
            
            #parses else-if block statements until next MEBBE, NO WAI, or OIC
            while self.current_token and not self.match(TokenType.MEBBE, TokenType.NO_WAI, TokenType.OIC):
                self.parse_statement()
        
        #parses else (NO WAI) block if present
        if self.match(TokenType.NO_WAI):
            self.advance()  #moves past NO WAI
            
            #parses else block statements until OIC
            while self.current_token and not self.match(TokenType.OIC):
                self.parse_statement()
        
        #end of conditional
        self.expect(TokenType.OIC, "Conditional must end with OIC")

    def parse_switch(self):
        #parses switch statement: WTF? → OMG cases [OMGWTF default] → OIC
        self.expect(TokenType.WTF)
        
        #must have at least one case
        if not self.match(TokenType.OMG):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"WTF? must be followed by at least one OMG case on line {line_num}")
        
        #parse all cases
        while self.match(TokenType.OMG):
            self.advance()  #moves past OMG
            
            #case value must be a literal (number, string, boolean, or null)
            if not self.match(TokenType.NUMBR, TokenType.NUMBAR, TokenType.YARN, TokenType.TROOF, TokenType.NOOB):
                line_num = self.current_token[2] if self.current_token else "EOF"
                raise SyntaxError(f"OMG must be followed by a literal value on line {line_num}")
            
            self.advance()  #moves past the literal value
            
            #parses case body statements until next OMG, OMGWTF, or OIC
            while self.current_token and not self.match(TokenType.OMG, TokenType.OMGWTF, TokenType.OIC):
                self.parse_statement()
        
        #parses default case (OMGWTF) if present
        if self.match(TokenType.OMGWTF):
            self.advance()  #moves past OMGWTF
            
            #parses default case statements until OIC
            while self.current_token and not self.match(TokenType.OIC):
                self.parse_statement()
        
        #end of switch statement
        self.expect(TokenType.OIC, "Switch statement must end with OIC")

    def parse_loop(self):
        #parses loop: IM IN YR label → UPPIN/NERFIN → YR variable → [TIL/WILE condition] → body → IM OUTTA YR label
        self.expect(TokenType.IM_IN_YR)
        
        #gets loop label name
        if not self.match(TokenType.LABEL):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected loop label after 'IM IN YR' on line {line_num}")
        
        label_name = self.current_token[0]
        self.advance()  #moves past label
        
        #loop must specify increment type (UPPIN = increment, NERFIN = decrement)
        if not self.match(TokenType.UPPIN, TokenType.NERFIN):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected UPPIN or NERFIN after loop label on line {line_num}")
        
        self.advance()  #moves past UPPIN/NERFIN
        
        #expects YR keyword before loop variable
        self.expect(TokenType.YR, "Expected YR after UPPIN/NERFIN")
        
        #gets the loop variable to increment/decrement
        self.expect(TokenType.VARIDENT, "Expected variable identifier after YR")
        
        #optional loop condition (TIL = until, WILE = while)
        if self.match(TokenType.TIL, TokenType.WILE):
            self.advance()  #moves past TIL/WILE
            self.parse_expression()  # Parse the loop condition
        
        #parses loop body statements until IM OUTTA YR
        while self.current_token and not self.match(TokenType.IM_OUTTA_YR):
            self.parse_statement()
        
        #verifies loop ends with matching label
        self.expect(TokenType.IM_OUTTA_YR, "Loop must end with IM OUTTA YR")
        
        if not self.match(TokenType.LABEL):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected loop label after 'IM OUTTA YR' on line {line_num}")
        
        end_label = self.current_token[0]
        if end_label != label_name: #checks if loop name at start and end are the same
            line_num = self.current_token[2]
            raise SyntaxError(f"Loop label mismatch: started with '{label_name}' but ended with '{end_label}' on line {line_num}")
        
        self.advance()  #moves past end label

    def parse_function_definition(self):
        #parses function definition: HOW IZ I function_name [YR parameters] → statements → IF U SAY SO
        self.expect(TokenType.HOW_IZ_I)
        
        #gets function name
        if not self.match(TokenType.FUNCIDENT):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected function identifier after 'HOW IZ I' on line {line_num}")
        
        self.advance()  #moves past function name
        
        #parses parameters if present (YR param1 AN YR param2 ...)
        if self.match(TokenType.YR):
            self.parse_parameter_list()
        
        #parses function body statements until IF U SAY SO
        while self.current_token and not self.match(TokenType.IF_U_SAY_SO):
            self.parse_statement()
        
        #ends function definition
        self.expect(TokenType.IF_U_SAY_SO, "Function must end with IF U SAY SO")

    def parse_parameter_list(self):
        #parses function parameters: YR param_name [AN YR param_name ...]
        self.expect(TokenType.YR)
        self.expect(TokenType.VARIDENT, "Expected parameter name after YR")
        
        #parses additional parameters separated by AN YR
        while self.match(TokenType.AN):
            self.advance()  #moves past AN
            self.expect(TokenType.YR, "Expected YR after AN in parameter list")
            self.expect(TokenType.VARIDENT, "Expected parameter name after YR")

    def parse_function_call(self):
        #parses function call: I IZ function_name [YR arguments] MKAY
        self.expect(TokenType.I_IZ)
        
        #gets function name to call
        if not self.match(TokenType.FUNCIDENT):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected function identifier after 'I IZ' on line {line_num}")
        
        self.advance()  #moves past function name
        
        #parses arguments if present (YR expr AN YR expr ...)
        if self.match(TokenType.YR):
            self.parse_argument_list()
        
        #ends function call
        self.expect(TokenType.MKAY, "Function call must end with MKAY")

    def parse_argument_list(self):
        #parses function arguments: YR expression [AN YR expression ...]
        self.expect(TokenType.YR)
        self.parse_expression()  #parses first argument expression
        
        #parses additional arguments separated by AN YR
        while self.match(TokenType.AN):
            self.advance()  #moves past AN
            self.expect(TokenType.YR, "Expected YR after AN in argument list")
            self.parse_expression()  #parses next argument expression

    def parse_return_statement(self):
        #parses return statement: FOUND YR expression
        self.expect(TokenType.FOUND_YR)
        self.parse_expression()  #parses the return value expression