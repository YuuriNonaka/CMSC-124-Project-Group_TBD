from lexer.lol_tokens import TokenType
from parser.ast_nodes import *


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
        
        program_node = self.parse_program() #constructs ast for entire program
        
        #ensures no extra tokens remain after the program ends
        if self.current_token:
            line_num = self.current_token[2]
            raise SyntaxError(
                f"Unexpected code after KTHXBYE on line {line_num}. "
                f"Program must end with KTHXBYE."
            )
        
        return program_node #returns complete ast

    def parse_program(self):
        #parses required program structure: HAI [version] [body] KTHXBYE
        self.expect(TokenType.HAI, "Program must start with HAI")
        
        program_node = ProgramNode() #creates root ast node
        
        #optional version number after HAI (may be omitted)
        if self.match(TokenType.NUMBAR):
            version_token = self.current_token
            program_node.version = version_token[0] #stores version number
            self.advance()  #moves past version number
        
        #parses the main body content
        statements = self.parse_main_body() #gets list of statement nodes
        program_node.statements = statements #stores statements in program node
        
        #program must end with KTHXBYE
        self.expect(TokenType.KTHXBYE, "Program must end with KTHXBYE")
        
        return program_node #returns complete program ast

    def parse_main_body(self):
        #optional variable declarations using wazzup, followed by statements
        statements = [] #collects all statement nodes
        
        if self.match(TokenType.WAZZUP):
            var_decls = self.parse_wazzup_block() #gets variable declaration nodes
            statements.extend(var_decls) #adds declarations to statement list
        
        #parses all statements until we reach KTHXBYE
        while self.current_token and not self.match(TokenType.KTHXBYE):
            stmt = self.parse_statement() #gets statement node
            if stmt: #only add non-none statements
                statements.append(stmt)
        
        return statements #returns list of statement nodes

    def parse_wazzup_block(self):
        #parses variable declaration block: WAZZUP [declarations] BUHBYE
        self.expect(TokenType.WAZZUP)
        
        declarations = [] #collects declaration nodes
        
        #parses all variable declarations until BUHBYE marker
        while self.current_token and not self.match(TokenType.BUHBYE):
            if self.match(TokenType.I_HAS_A):
                decl_node = self.parse_variable_declaration() #gets declaration node
                declarations.append(decl_node)
            else:
                line_num = self.current_token[2]
                raise SyntaxError(
                    f"Expected variable declaration (I HAS A) or BUHBYE in WAZZUP block, "
                    f"but got '{self.current_token[0]}' on line {line_num}"
                )
        
        self.expect(TokenType.BUHBYE, "WAZZUP block must end with BUHBYE")
        
        return declarations #returns list of declaration nodes

    def parse_variable_declaration(self):
        #parses variable declarations: I HAS A <variable> [ITZ <initial value>]
        self.expect(TokenType.I_HAS_A)
        
        #requires a variable identifier after I HAS A
        if not self.match(TokenType.VARIDENT):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(
                f"Expected variable identifier after 'I HAS A' on line {line_num}"
            )
        
        var_name = self.current_token[0] #stores variable name
        self.advance()  #move past variable name
        
        initial_value = None #default no initialization
        
        #optional initialization with ITZ keyword
        if self.match(TokenType.ITZ):
            self.advance()  #moves past ITZ
            initial_value = self.parse_expression() #gets initial value expression node
        
        return VariableDeclNode(var_name, initial_value) #returns declaration node

    def parse_statement(self):
        #parses one statement: output, input, assignment, conditionals, loops, functions, etc.
        #has separate functions for each type
        if not self.current_token:
            return None
        
        token_type = self.current_token[1]
        line_num = self.current_token[2]
        
        #VISIBLE - output statement
        if token_type == TokenType.VISIBLE:
            return self.parse_visible_statement() #returns visible node
        
        #GIMMEH - input statement  
        elif token_type == TokenType.GIMMEH:
            return self.parse_gimmeh_statement() #returns gimmeh node
        
        #Assignment: <variable> R <expression>
        elif token_type == TokenType.VARIDENT:
            return self.parse_assignment_or_expression() #returns assignment or variable node
        
        #O RLY? - if/else conditional
        elif token_type == TokenType.O_RLY:
            return self.parse_conditional() #returns conditional node
        
        #WTF? - switch/case statement
        elif token_type == TokenType.WTF:
            return self.parse_switch() #returns switch node
        
        #IM IN YR - loop construct
        elif token_type == TokenType.IM_IN_YR:
            return self.parse_loop() #returns loop node
        
        #HOW IZ I - function definition
        elif token_type == TokenType.HOW_IZ_I:
            return self.parse_function_definition() #returns function definition node
        
        #I IZ - function call
        elif token_type == TokenType.I_IZ:
            return self.parse_function_call() #returns function call node
        
        #FOUND YR - return from function
        elif token_type == TokenType.FOUND_YR:
            return self.parse_return_statement() #returns return node
        
        #GTFO - break out of loop or switch
        elif token_type == TokenType.GTFO:
            self.advance()  #moves past GTFO token
            return BreakNode() #returns break node
        
        #expression that evaluates to IT variable
        elif self.is_expression_start():
            return self.parse_expression() #returns expression node
        
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
        
        expressions = [] #collects expression nodes to output
        
        #parses first expression
        expr = self.parse_expression() #gets expression node
        expressions.append(expr)
        
        #parses additional expressions on the same line (space-separated)
        while self.current_token and self.is_expression_start() and self.current_token[1] != TokenType.LINEBREAK:
            expr = self.parse_expression() #gets expression node
            expressions.append(expr)
        
        #consumes the line break at the end of the statement if present
        if self.current_token and self.current_token[1] == TokenType.LINEBREAK:
            self.advance()
        
        return VisibleNode(expressions) #returns visible node with expressions

    def parse_gimmeh_statement(self):
        #parses GIMMEH statement: read input into a variable
        self.expect(TokenType.GIMMEH)
        var_token = self.expect(TokenType.VARIDENT, "GIMMEH requires a variable identifier")
        return GimmehNode(var_token[0]) #returns gimmeh node with variable name

    def parse_assignment_or_expression(self):
        #parses either variable assignment (<var> R <expr>) or variable reference as expression
        var_token = self.current_token
        var_name = var_token[0] #stores variable name
        self.advance()  #moves past variable name
        
        if self.match(TokenType.R):
            #this is an assignment: variable R expression
            self.advance()  #moves past R token
            expr = self.parse_expression() #gets expression node
            return AssignmentNode(var_name, expr) #returns assignment node
        else:
            #if no R token, this is just a variable reference (valid as standalone expression)
            return VariableNode(var_name) #returns variable reference node

    def parse_conditional(self):
        #parses if/else conditional: O RLY? → YA RLY [MEBBE] [NO WAI] → OIC
        self.expect(TokenType.O_RLY)
        
        conditional_node = ConditionalNode() #creates conditional node
        
        #requires if block
        self.expect(TokenType.YA_RLY, "O RLY? must be followed by YA RLY")
        
        #parses statements until MEBBE (else if), NO WAI (else), or OIC (end)
        while self.current_token and not self.match(TokenType.MEBBE, TokenType.NO_WAI, TokenType.OIC):
            stmt = self.parse_statement() #gets statement node
            if stmt:
                conditional_node.if_block.append(stmt) #adds to if block
        
        #parse any else-if (MEBBE) blocks
        while self.match(TokenType.MEBBE):
            self.advance()  #moves MEBBE
            condition = self.parse_expression()  #parse the condition
            
            elif_clause = ElifClauseNode(condition) #creates elif clause node
            
            #parses else-if block statements until next MEBBE, NO WAI, or OIC
            while self.current_token and not self.match(TokenType.MEBBE, TokenType.NO_WAI, TokenType.OIC):
                stmt = self.parse_statement() #gets statement node
                if stmt:
                    elif_clause.statements.append(stmt) #adds to elif block
            
            conditional_node.elif_blocks.append(elif_clause) #adds elif clause to conditional
        
        #parses else (NO WAI) block if present
        if self.match(TokenType.NO_WAI):
            self.advance()  #moves past NO WAI
            
            #parses else block statements until OIC
            while self.current_token and not self.match(TokenType.OIC):
                stmt = self.parse_statement() #gets statement node
                if stmt:
                    conditional_node.else_block.append(stmt) #adds to else block
        
        #end of conditional
        self.expect(TokenType.OIC, "Conditional must end with OIC")
        
        return conditional_node #returns complete conditional node

    def parse_switch(self):
        #parses switch statement: WTF? → OMG cases [OMGWTF default] → OIC
        self.expect(TokenType.WTF)
        
        switch_node = SwitchNode() #creates switch node
        
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
            
            literal_value = self.current_token[0] #stores case value
            self.advance()  #moves past the literal value
            
            case_node = CaseNode(literal_value) #creates case node
            
            #parses case body statements until next OMG, OMGWTF, or OIC
            while self.current_token and not self.match(TokenType.OMG, TokenType.OMGWTF, TokenType.OIC):
                stmt = self.parse_statement() #gets statement node
                if stmt:
                    case_node.statements.append(stmt) #adds to case block
            
            switch_node.cases.append(case_node) #adds case to switch
        
        #parses default case (OMGWTF) if present
        if self.match(TokenType.OMGWTF):
            self.advance()  #moves past OMGWTF
            
            #parses default case statements until OIC
            while self.current_token and not self.match(TokenType.OIC):
                stmt = self.parse_statement() #gets statement node
                if stmt:
                    switch_node.default_case.append(stmt) #adds to default case
        
        #end of switch statement
        self.expect(TokenType.OIC, "Switch statement must end with OIC")
        
        return switch_node #returns complete switch node

    def parse_loop(self):
        #parses loop: IM IN YR label → UPPIN/NERFIN → YR variable → [TIL/WILE condition] → body → IM OUTTA YR label
        self.expect(TokenType.IM_IN_YR)
        
        #gets loop label name
        if not self.match(TokenType.LABEL):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected loop label after 'IM IN YR' on line {line_num}")
        
        label_name = self.current_token[0] #stores label name
        self.advance()  #moves past label
        
        #loop must specify increment type (UPPIN = increment, NERFIN = decrement)
        if not self.match(TokenType.UPPIN, TokenType.NERFIN):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected UPPIN or NERFIN after loop label on line {line_num}")
        
        operation = self.current_token[0] #stores operation type
        self.advance()  #moves past UPPIN/NERFIN
        
        #expects YR keyword before loop variable
        self.expect(TokenType.YR, "Expected YR after UPPIN/NERFIN")
        
        #gets the loop variable to increment/decrement
        var_token = self.expect(TokenType.VARIDENT, "Expected variable identifier after YR")
        var_name = var_token[0] #stores variable name
        
        loop_node = LoopNode(label_name, operation, var_name) #creates loop node
        
        #optional loop condition (TIL = until, WILE = while)
        if self.match(TokenType.TIL, TokenType.WILE):
            condition_type = self.current_token[0] #stores condition type
            self.advance()  #moves past TIL/WILE
            condition = self.parse_expression()  # Parse the loop condition
            loop_node.condition = condition #stores condition expression
            loop_node.condition_type = condition_type #stores til or wile
        
        #parses loop body statements until IM OUTTA YR
        while self.current_token and not self.match(TokenType.IM_OUTTA_YR):
            stmt = self.parse_statement() #gets statement node
            if stmt:
                loop_node.statements.append(stmt) #adds to loop body
        
        #verifies loop ends with matching label
        self.expect(TokenType.IM_OUTTA_YR, "Loop must end with IM OUTTA YR")
        
        if not self.match(TokenType.LABEL):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected loop label after 'IM OUTTA YR' on line {line_num}")
        
        end_label = self.current_token[0] #stores end label
        if end_label != label_name: #checks if loop name at start and end are the same
            line_num = self.current_token[2]
            raise SyntaxError(f"Loop label mismatch: started with '{label_name}' but ended with '{end_label}' on line {line_num}")
        
        self.advance()  #moves past end label
        
        return loop_node #returns complete loop node

    def parse_function_definition(self):
        #parses function definition: HOW IZ I function_name [YR parameters] → statements → IF U SAY SO
        self.expect(TokenType.HOW_IZ_I)
        
        #gets function name
        if not self.match(TokenType.FUNCIDENT):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected function identifier after 'HOW IZ I' on line {line_num}")
        
        func_name = self.current_token[0] #stores function name
        self.advance()  #moves past function name
        
        parameters = [] #collects parameter names
        
        #parses parameters if present (YR param1 AN YR param2 ...)
        if self.match(TokenType.YR):
            parameters = self.parse_parameter_list() #gets list of parameter names
        
        func_node = FunctionDefNode(func_name, parameters) #creates function definition node
        
        #parses function body statements until IF U SAY SO
        while self.current_token and not self.match(TokenType.IF_U_SAY_SO):
            stmt = self.parse_statement() #gets statement node
            if stmt:
                func_node.statements.append(stmt) #adds to function body
        
        #ends function definition
        self.expect(TokenType.IF_U_SAY_SO, "Function must end with IF U SAY SO")
        
        return func_node #returns complete function definition node

    def parse_parameter_list(self):
        #parses function parameters: YR param_name [AN YR param_name ...]
        self.expect(TokenType.YR)
        param_token = self.expect(TokenType.VARIDENT, "Expected parameter name after YR")
        parameters = [param_token[0]] #stores first parameter name
        
        #parses additional parameters separated by AN YR
        while self.match(TokenType.AN):
            self.advance()  #moves past AN
            self.expect(TokenType.YR, "Expected YR after AN in parameter list")
            param_token = self.expect(TokenType.VARIDENT, "Expected parameter name after YR")
            parameters.append(param_token[0]) #adds parameter name to list
        
        return parameters #returns list of parameter names

    def parse_function_call(self):
        #parses function call: I IZ function_name [YR arguments] MKAY
        self.expect(TokenType.I_IZ)
        
        #gets function name to call
        if not self.match(TokenType.FUNCIDENT):
            line_num = self.current_token[2] if self.current_token else "EOF"
            raise SyntaxError(f"Expected function identifier after 'I IZ' on line {line_num}")
        
        func_name = self.current_token[0] #stores function name
        self.advance()  #moves past function name
        
        arguments = [] #collects argument expressions
        
        #parses arguments if present (YR expr AN YR expr ...)
        if self.match(TokenType.YR):
            arguments = self.parse_argument_list() #gets list of argument nodes
        
        #ends function call
        self.expect(TokenType.MKAY, "Function call must end with MKAY")
        
        return FunctionCallNode(func_name, arguments) #returns function call node

    def parse_argument_list(self):
        #parses function arguments: YR expression [AN YR expression ...]
        self.expect(TokenType.YR)
        expr = self.parse_expression()  #parses first argument expression
        arguments = [expr] #stores first argument node
        
        #parses additional arguments separated by AN YR
        while self.match(TokenType.AN):
            self.advance()  #moves past AN
            self.expect(TokenType.YR, "Expected YR after AN in argument list")
            expr = self.parse_expression()  #parses next argument expression
            arguments.append(expr) #adds argument node to list
        
        return arguments #returns list of argument nodes

    def parse_return_statement(self):
        #parses return statement: FOUND YR expression
        self.expect(TokenType.FOUND_YR)
        expr = self.parse_expression()  #parses the return value expression
        return ReturnNode(expr) #returns return node with expression

    def is_expression_start(self):
        #checks if current token can begin an expression (literals, variables, operators, etc.)
        if not self.current_token:
            return False
        
        return self.match(
            #literal values
            TokenType.NUMBR, TokenType.NUMBAR, TokenType.YARN,
            TokenType.TROOF, TokenType.NOOB,
            #variable references
            TokenType.VARIDENT,
            #math operators
            TokenType.SUM_OF, TokenType.DIFF_OF, TokenType.PRODUKT_OF,
            TokenType.QUOSHUNT_OF, TokenType.MOD_OF,
            TokenType.BIGGR_OF, TokenType.SMALLR_OF,
            #boolean operators
            TokenType.BOTH_OF, TokenType.EITHER_OF, TokenType.WON_OF,
            TokenType.NOT, TokenType.ALL_OF, TokenType.ANY_OF,
            #comparison operators
            TokenType.BOTH_SAEM, TokenType.DIFFRINT,
            #string concatenation
            TokenType.SMOOSH,
            #type casting
            TokenType.MAEK,
            #function calls
            TokenType.I_IZ,
            #string delimiters
            TokenType.STRING_DELIM
        )

    def parse_expression(self):
        #parses expressions: literals, variables, operations, function calls, etc.
        if not self.current_token:
            raise SyntaxError("Unexpected end of file in expression")
        
        token_type = self.current_token[1]
        
        #simple literals: numbers, strings, booleans, null
        if token_type in (TokenType.NUMBR, TokenType.NUMBAR, TokenType.YARN,
                        TokenType.TROOF, TokenType.NOOB):
            value = self.current_token[0] #stores literal value
            self.advance()
            return LiteralNode(value, token_type) #returns literal node
        
        #string with quotes: "content"
        if token_type == TokenType.STRING_DELIM:
            self.advance()  #moves past opening quote
            string_parts = [] #collects string content
            #parses string content (YARN tokens between quotes)
            while self.current_token and self.current_token[1] != TokenType.STRING_DELIM:
                if self.current_token[1] == TokenType.YARN:
                    string_parts.append(self.current_token[0]) #adds content
                    self.advance()
                else:
                    break
            #ensures closing quote exists
            if not self.match(TokenType.STRING_DELIM):
                line_num = self.current_token[2] if self.current_token else "EOF"
                raise SyntaxError(f"Unterminated string literal on line {line_num}")
            self.advance()  #move past closing quote
            string_value = ' '.join(string_parts) #combines string content
            return LiteralNode(string_value, TokenType.YARN) #returns string literal node
        
        #variable reference
        if token_type == TokenType.VARIDENT:
            var_name = self.current_token[0] #stores variable name
            self.advance()
            return VariableNode(var_name) #returns variable node
        
        #math operations: SUM OF expr AN expr
        if token_type in (TokenType.SUM_OF, TokenType.DIFF_OF, TokenType.PRODUKT_OF,
                        TokenType.QUOSHUNT_OF, TokenType.MOD_OF,
                        TokenType.BIGGR_OF, TokenType.SMALLR_OF):
            operator = self.current_token[0] #stores operator
            self.advance()  #moves past operator
            left = self.parse_expression()  #parses first operand
            self.expect(TokenType.AN, "Binary operator requires AN between operands")
            right = self.parse_expression()  #parses second operand
            return BinaryOpNode(operator, left, right) #returns binary operation node
        
        #binary boolean operations: BOTH OF expr AN expr
        if token_type in (TokenType.BOTH_OF, TokenType.EITHER_OF, TokenType.WON_OF):
            operator = self.current_token[0] #stores operator
            self.advance()  #moves past operator
            left = self.parse_expression()  #parses first operand
            self.expect(TokenType.AN, "Binary operator requires AN between operands")
            right = self.parse_expression()  #parses second operand
            return BinaryOpNode(operator, left, right) #returns binary operation node
        
        #NOT operation: NOT expr
        if token_type == TokenType.NOT:
            operator = self.current_token[0] #stores operator
            self.advance()  #moves past NOT
            operand = self.parse_expression()  #parses operand
            return UnaryOpNode(operator, operand) #returns unary operation node
        
        #multi-argument operations: ALL OF expr AN expr AN expr ... MKAY
        if token_type in (TokenType.ALL_OF, TokenType.ANY_OF, TokenType.SMOOSH):
            operator = self.current_token[0] #stores operator
            self.advance()  #moves past operator
            
            operands = [] #collects operands
            
            #parses at least one operand
            operands.append(self.parse_expression()) #adds first operand
            
            #parses additional operands separated by AN
            while self.match(TokenType.AN):
                self.advance()  #moves past AN
                operands.append(self.parse_expression()) #adds operand
            
            #ends multi-argument operation with MKAY
            self.expect(TokenType.MKAY, f"{token_type.value} must end with MKAY")
            return InfiniteArityOpNode(operator, operands) #returns infinite arity operation node
        
        #comparison operations: BOTH SAEM expr AN expr
        if token_type in (TokenType.BOTH_SAEM, TokenType.DIFFRINT):
            operator = self.current_token[0] #stores operator
            self.advance()  #moves past operator
            left = self.parse_expression()  #parses first operand
            self.expect(TokenType.AN, "Comparison operator requires AN between operands")
            right = self.parse_expression()  #parses second operand
            return ComparisonNode(operator, left, right) #returns comparison node
        
        #type casting: MAEK expression [A] type_keyword
        if token_type == TokenType.MAEK:
            self.advance()  #moves past MAEK
            expr = self.parse_expression()  #parses expression to cast
            
            #optional A keyword before type
            if self.match(TokenType.A):
                self.advance()
            
            #requires type keyword (NUMBR, NUMBAR, YARN, TROOF, NOOB)
            if not self.match(TokenType.TYPE_NUMBR, TokenType.TYPE_NUMBAR,
                            TokenType.TYPE_YARN, TokenType.TYPE_TROOF, TokenType.TYPE_NOOB):
                line_num = self.current_token[2] if self.current_token else "EOF"
                raise SyntaxError(f"Expected type keyword after MAEK on line {line_num}")
            
            target_type = self.current_token[0] #stores target type
            self.advance()  #moves past type keyword
            return TypecastNode(expr, target_type) #returns typecast node
        
        #function call within expression
        if token_type == TokenType.I_IZ:
            return self.parse_function_call() #returns function call node
        
        #invalid expression start, prints error message
        line_num = self.current_token[2]
        raise SyntaxError(
            f"Invalid expression starting with '{self.current_token[0]}' on line {line_num}"
        )

def parse_tokens(tokens): #function to simplify use in gui code
    parser = Parser(tokens)
    ast = parser.parse() #gets ast instead of just true
    return ast #returns ast for potential use