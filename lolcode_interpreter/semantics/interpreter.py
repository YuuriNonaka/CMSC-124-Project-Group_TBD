import operator
from parser.ast_nodes import *
from lexer.lol_tokens import TokenType
from semantics import bool_convert

def lol_to_num(value):
    if value == "WIN":
        return 1
    if value == "FAIL":
        return 0
    if value == "NOOB":
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

def interpret(node, gui_print, gui_input):
    symbol_table = {'IT': 'NOOB'}

    function_table = {}

    for statement in node.statements:
        if isinstance(statement, FunctionDefNode):
            function_table[statement.func_name] = statement
    
    for statement in node.statements:
        if not isinstance(statement, FunctionDefNode):
            execute_statement(statement, symbol_table, function_table, gui_print, gui_input)
    
    # print(symbol_table)
    return symbol_table

# the statement passed as the node will be performed
def execute_statement(node, symbol_table, function_table, gui_print, gui_input):
    
    if isinstance(node, VariableDeclNode):
        value = "NOOB" # default value for variables without values
        if node.initial_value:
            value = evaluate_expression(node.initial_value, symbol_table, function_table, gui_print, gui_input)
        symbol_table[node.var_name] = value
    
    elif isinstance(node, AssignmentNode):
        if node.var_name not in symbol_table:
            # variable not declared
            return
        value = evaluate_expression(node.expression, symbol_table, function_table, gui_print, gui_input)
        symbol_table[node.var_name] = value
    
    elif isinstance(node, VisibleNode):
        outputs = []
        last_value = "NOOB"
        for expression in node.expressions:
            last_value = evaluate_expression(expression, symbol_table, function_table, gui_print, gui_input)
            outputs.append(lol_to_str(last_value))

        output_string = "".join(outputs)
        gui_print(output_string + "\n")
        symbol_table["IT"] = last_value    

    elif isinstance(node, GimmehNode):
        if node.var_name not in symbol_table:
            pass

        user_input = gui_input()
        if user_input is None:
            user_input = "NOOB" #default value
        symbol_table[node.var_name] = user_input
    
    else:
        val = evaluate_expression(node, symbol_table, function_table, gui_print, gui_input)
        symbol_table["IT"] = val

# evaluate the node, return value
def evaluate_expression(node, symbol_table, function_table, gui_print, gui_input):

    if isinstance(node, LiteralNode):
        if node.literal_type == TokenType.NUMBR:
            return int(node.value)
        if node.literal_type == TokenType.NUMBAR:
            return float(node.value)
        if node.literal_type == TokenType.YARN:
            return str(node.value)
        if node.literal_type == TokenType.TROOF:
            return node.value == "WIN"
        if node.literal_type == TokenType.NOOB:
            return "NOOB"
    
    elif isinstance(node, VariableNode):
        value = symbol_table.get(node.var_name, "NOOB")
        return value
    
    elif isinstance(node, BinaryOpNode):
        left_op = evaluate_expression(node.left, symbol_table, function_table, gui_print, gui_input)
        right_op = evaluate_expression(node.right, symbol_table, function_table, gui_print, gui_input)

        operations = {
            "SUM OF": operator.add,
            "DIFF OF": operator.sub,
            "PRODUKT OF": operator.mul,
            "QUOSHUNT OF": operator.truediv,
            "MOD OF": operator.mod,
            "BIGGR OF": max,
            "SMALLR OF": min,
            "BOTH OF": lambda first_op, second_op: bool_convert(first_op) and bool_convert(second_op),
            "EITHER OF": lambda first_op, second_op: bool_convert(first_op) or bool_convert(second_op),
            "WON OF": lambda first_op, second_op: bool_convert(first_op) ^ bool_convert(second_op),
            "BOTH SAEM": operator.eq,
            "DIFFRINT": operator.ne,
        }

        operator_function = operations.get(node.operator)

        if node.operator not in ["BOTH OF", "EITHER OF", "WON OF"]:
            # this will be a math oepration
            left_op = lol_to_num(left_op)
            right_op = lol_to_num(right_op)
        
        result = operator_function(left_op, right_op)
        return format_result(result)
    
    elif isinstance(node, ComparisonNode):
        left_op = lol_to_str(evaluate_expression(node.left, symbol_table, function_table, gui_print, gui_input))
        right_op = lol_to_str(evaluate_expression(node.right, symbol_table, function_table, gui_print, gui_input))

        if node.operator == "BOTH SAEM":
            result = (left_op == right_op)
        elif node.operator == "DIFFRINT":
            result = (left_op != right_op)
        return format_result(result)
    
    elif isinstance(node, UnaryOpNode):
        value = evaluate_expression(node.operand, symbol_table, function_table, gui_print, gui_input)
        result = not bool_convert(value)
        return format_result(result)
    
    elif isinstance(node, InfiniteArityOpNode):
        operands = [evaluate_expression(op, symbol_table, function_table, gui_print, gui_input) for op in node.operands]

        if node.operator == "SMOOSH":
            return "".join([lol_to_str(op) for op in operands])
        
        if node.operator == "ALL OF":
            result = all(bool_convert(op) for op in operands)
            return format_result(result)

        if node.operator == "ANY OF":
            result = any(bool_convert(op) for op in operands)
            return format_result(result)
    else:
        pass
        # print("Error")