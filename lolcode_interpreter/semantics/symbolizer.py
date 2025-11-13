from lexer.lol_tokens import TokenType
import operator

def bool_convert(token):
    if token == "NOOB" or token == "" or token == 0 or token == "FAIL":
        return False
    else:
        return True

def get_value(tokens, symbol_table): #helper function: converts expression into a single string value ("noot noot" var => noot noot 12)
    
    if not tokens: 
        return "NOOB"
    
    # this block simply gets the actualy value of the token
    if len(tokens) == 1:
        lexeme, token_type, line_num = tokens[0]

        # print(f"{lexeme} - {token_type} - {line_num}")

        if token_type == TokenType.NUMBR:
            return int(lexeme)
        if token_type == TokenType.NUMBAR:
            return float(lexeme)
        if token_type == TokenType.YARN:
            return lexeme
        if token_type == TokenType.TROOF:
            if lexeme == "WIN":
                return True
            else:
                return False
        if token_type == TokenType.NOOB:
            return "NOOB"
        if token_type == TokenType.VARIDENT:
            value = symbol_table.get(lexeme, "")
            try:
                return int(value)
            except(ValueError, TypeError):
                try:
                    return float(value)
                except(ValueError, TypeError):
                    return str(value)
        else:
            return lexeme
    
    # operators
    operator_lexeme, operator_type, operator_num = tokens[0]
    operations = {
        TokenType.SUM_OF: operator.add,
        TokenType.DIFF_OF: operator.sub,
        TokenType.PRODUKT_OF: operator.mul,
        TokenType.QUOSHUNT_OF: operator.truediv,
        TokenType.MOD_OF: operator.mod,
        TokenType.BIGGR_OF: max,
        TokenType.SMALLR_OF: min,
        TokenType.BOTH_OF: lambda first_op, second_op: bool_convert(first_op) and bool_convert(second_op),
        TokenType.EITHER_OF: lambda first_op, second_op: bool_convert(first_op) or bool_convert(second_op),
        TokenType.WON_OF: lambda first_op, second_op: bool_convert(first_op) ^ bool_convert(second_op),
        TokenType.BOTH_SAEM: operator.eq,
        TokenType.DIFFRINT: operator.ne,
    }

    # yarn hadnling
    if ((len(tokens) == 3) and
        (tokens[0][1] == TokenType.STRING_DELIM) and
        (tokens[1][1] == TokenType.YARN) and
        (tokens[2][1] == TokenType.STRING_DELIM)):
        return tokens[1][0]
    
    # not 
    if operator_type == TokenType.NOT:
        operands = tokens[1:]
        values = get_value(operands, symbol_table)
        return (not bool_convert(values))

    if operator_type in operations:
        AN_index = -1
        # reverse is for nested expressions
        for i, (lexeme, token_type, line_num) in enumerate(reversed(tokens)):
            if token_type == TokenType.AN:
                AN_index = len(tokens) - 1 - i
                break
        
        if AN_index == -1: # AN not found
            return "NOOB"
        
        first_op = tokens[1:AN_index]
        second_op = tokens[AN_index+1:]

        value1 = get_value(first_op, symbol_table)
        value2 = get_value(second_op, symbol_table)

        try:
            operate = operations[operator_type]

            # bool to 1 (win) or 0 (fail)
            if value1 == "WIN" or value1 == True:
                value1 = 1
            if value2 == "WIN" or value2 == True:
                value2 = 1
            if value1 == "FAIL" or value1 == False:
                value1 = 0
            if value2 == "FAIL" or value2 == False:
                value2 = 0         
            if operator_type == TokenType.BOTH_SAEM or operator_type == TokenType.DIFFRINT:
                value1 = str(value1)
                value2 = str(value2)

            result =  operate(value1, value2)
            if isinstance(result, bool):
                if result: #if true
                    return "WIN"
                else:
                    return "FAIL"
            
            return result
                
        except Exception:
            return "NOOB"
    
    # string concatenation
    if operator_type == TokenType.SMOOSH:
        AN_index = -1
        # reverse is for nested expressions
        for i, (lexeme, token_type, line_num) in enumerate(reversed(tokens)):
            if token_type == TokenType.AN:
                AN_index = len(tokens) - 1 - i
                break

        if AN_index == -1: # AN not found
            return "NOOB"
    
        first_op = tokens[1:AN_index]
        second_op = tokens[AN_index+1:]

        value1 = str(get_value(first_op, symbol_table))
        value2 = str(get_value(second_op, symbol_table))
        concatval = value1 + value2

        return concatval

    return get_value([tokens[0]], symbol_table)

def symbolize(tokens):
    symbol_table = {}
    symbol_table['IT'] = "NOOB"

    i = 0
    while i < len(tokens):
        lexeme, token_type, line_num = tokens[i]

        # I HAS A <var> ITZ <value>
        if ((token_type == TokenType.I_HAS_A) and 
            (i + 3 < len(tokens)) and # value exists after the ITZ
            (tokens[i + 1][1] == TokenType.VARIDENT) and # checks the variable
            (tokens[i + 2][1] == TokenType.ITZ)): # checks the assignment syntax ITZ

            var_name = tokens[i+1][0]
            
            value_tokens = []
            index = i + 3
            # scan until linebreak
            while index < len(tokens) and tokens[index][1] != TokenType.LINEBREAK:
                value_tokens.append(tokens[index])
                index += 1

            value = get_value(value_tokens, symbol_table)
            symbol_table[var_name] = value

            i = index
            continue

        # I HAS A <var> 
        elif ((token_type == TokenType.I_HAS_A) and
              (i + 1 < len(tokens)) and # variable exists
              (tokens[i + 1][1] == TokenType.VARIDENT)): # checks the variable
            
            var_name = tokens[i + 1][0]
            if var_name not in symbol_table:
                symbol_table[var_name] = "NOOB"
            
            index = i + 2
            while index < len(tokens) and tokens[index][1] != TokenType.LINEBREAK:
                index += 1

            i = index
            continue

        # reassigning var
        elif ((token_type == TokenType.VARIDENT) and
              (i + 2 < len(tokens)) and 
              (tokens[i + 1][1] == TokenType.R)):
            
            var_name = lexeme
            
            value_tokens = []
            index = i + 2
            while index < len(tokens) and tokens[index][1] != TokenType.LINEBREAK:
                value_tokens.append(tokens[index])
                index += 1

            value = get_value(value_tokens, symbol_table)

            if var_name in symbol_table:
                symbol_table[var_name] = value
            else:
                symbol_table[var_name] = value

            i = index
            continue

        # VISIBLE
        elif token_type == TokenType.VISIBLE:
            value_tokens = []
            index = i + 1
            while index < len(tokens) and tokens[index][1] != TokenType.LINEBREAK:
                value_tokens.append(tokens[index])
                index += 1
            
            value = get_value(value_tokens, symbol_table)

            if value == True:
                value = "WIN"
            if value == False:
                value = "FAIL"

            symbol_table["IT"] = value

            i = index
            continue
            
        i += 1
    
    return symbol_table