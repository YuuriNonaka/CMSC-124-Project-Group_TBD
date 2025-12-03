from lexer.lol_tokens import TokenType
from parser.ast_nodes import *
import operator

def bool_convert(token):
    if token == "NOOB" or token == "" or token == 0 or token == "FAIL":
        return False
    else:
        return True
    
class InterpreterRuntimeError(Exception):
    pass

class BreakNode(Exception):
    # GTFO / break statement
    pass 

class ReturnNode(Exception):
    # FOUND YR / return statement
    def __init__(self, value):
        self.value = value

def lol_to_num(value):
    if value == "WIN":
        return 1
    if value == "FAIL":
        return 0
    if value == "NOOB":
        return 0
    
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return value
    
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return 0

    try:
        return int(value)
    except(ValueError, TypeError):
        try:
            return float(value)
        except:
            return 0

def lol_to_str(value):
    if value is True:
        return "WIN"
    if value is False:
        return "FAIL"
    if value is None:
        return "NOOB"
    if value == "NOOB":
        return "NOOB"
    return str(value)

def format_result(value):
    if isinstance(value, bool):
        if value:
            return "WIN"
        else:
            return "FAIL"
    return value