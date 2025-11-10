from lexer import TokenType

def symbolize(tokens):
    symbol_table = {}
    symbol_table['IT'] = ""

    for i in range(len(tokens)):
        lexeme, token_type, line_num = tokens[i]

        # I HAS A <var> ITZ <value>
        if ((token_type == TokenType.I_HAS_A) and 
            (i + 3 < len(tokens)) and 
            (tokens[i + 1][1] == TokenType.VARIDENT) and 
            (tokens[i + 2][1] == TokenType.ITZ)):

            var_name = tokens[i+1][0]
            value = tokens[i+3][0]

            symbol_table[var_name] = value

            i += 4
            continue

        # I HAS A <var> 
        elif ((token_type == TokenType.I_HAS_A) and
              (i + 1 < len(tokens)) and
              (tokens[i + 1][1] == TokenType.VARIDENT)):
            
            var_name = tokens[i + 1][0]
            if var_name not in symbol_table:
                symbol_table[var_name] = ""
            
            i += 2
            continue
    
    return symbol_table