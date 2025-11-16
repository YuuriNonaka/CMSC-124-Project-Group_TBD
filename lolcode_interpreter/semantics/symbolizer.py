from lexer.lol_tokens import TokenType
import operator

def bool_convert(token):
    if token == "NOOB" or token == "" or token == 0 or token == "FAIL":
        return False
    else:
        return True