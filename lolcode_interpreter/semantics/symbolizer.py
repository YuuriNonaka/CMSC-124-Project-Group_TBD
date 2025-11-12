from lexer.lol_tokens import TokenType

def get_value(tokens, symbol_table): #helper function: converts expression into a single string value ("noot noot" var => noot noot 12)
    values = []
    for lexeme, token_type, line_num in tokens:
        if token_type == TokenType.YARN or token_type == TokenType.NUMBR or token_type == TokenType.NUMBAR or token_type == TokenType.TROOF:
            values.append(lexeme) #if simply a literal, just append.
        
        elif token_type == TokenType.VARIDENT:
            values.append(str(symbol_table.get(lexeme, ""))) #if a variable, find its value, turn into a string, and append.
        
        elif token_type == TokenType.STRING_DELIM:
            pass #delimiters are not included
    
    return " ".join(values)

def symbolize(tokens):
    symbol_table = {}
    symbol_table['IT'] = ""

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
                symbol_table[var_name] = ""
            
            index = i + 2
            while index < len(tokens) and tokens[index][1] != TokenType.LINEBREAK:
                index += 1

            i += index
            continue

        # VISIBLE
        elif token_type == TokenType.VISIBLE:
            value_tokens = []
            index = i + 1
            while index < len(tokens) and tokens[index][1] != TokenType.LINEBREAK:
                value_tokens.append(tokens[index])
                index += 1
            
            value = get_value(value_tokens, symbol_table)
            symbol_table["IT"] = value

            i = index
            continue
            
        i += 1
    
    return symbol_table