import operator
from parser.ast_nodes import *
from lexer.lol_tokens import TokenType
from semantics import bool_convert

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
    symbol_table = {'IT': 'NOOB'} # stores variables
 
    function_table = {} # all functions wil be placed here

    # stores all the functions
    for statement in node.statements:
        if isinstance(statement, FunctionDefNode):
            function_table[statement.func_name] = statement
    
    #execute statements
    for statement in node.statements:
        if not isinstance(statement, FunctionDefNode):
            execute_statement(statement, symbol_table, function_table, gui_print, gui_input)
    
    # print(symbol_table)
    return symbol_table

# the statement passed as the node will be performed
def execute_statement(node, symbol_table, function_table, gui_print, gui_input):
    
    if isinstance(node, VariableDeclNode): # I HAS A
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
    
    elif isinstance(node, VisibleNode): # VISIBLE
        outputs = []
        last_value = "NOOB"
        for expression in node.expressions: # loops for multiple arguments
            last_value = evaluate_expression(expression, symbol_table, function_table, gui_print, gui_input)
            outputs.append(lol_to_str(last_value))

        output_string = "".join(outputs) # smoosh
        gui_print(output_string + "\n") # for testing
        symbol_table["IT"] = last_value #shows the last value of the exp

    elif isinstance(node, GimmehNode): # GIMMEH
        if node.var_name not in symbol_table:
            pass # variable not declared

        user_input = gui_input() # FOR TESTING PURPOSES ONLY. INPUTS ARE DONE USING A DIALOGUE BOX
        if user_input is None:
            user_input = "NOOB" #default value
        symbol_table[node.var_name] = user_input

    elif isinstance(node, ConditionalNode):
        conditional_value = symbol_table.get("IT", "NOOB")

        if bool_convert(conditional_value): # YA RLY
            for statement in node.if_block:
                execute_statement(statement, symbol_table, function_table, gui_print, gui_input)
        
        else: # MEBBE
            executed_else_if = False
            for else_if_clause in node.elif_blocks:
                else_if_value = evaluate_expression(else_if_clause.condition, symbol_table, function_table, gui_print, gui_input)
                if bool_convert(else_if_value): # MEBBE conditions
                    for statement in else_if_clause.statements: #execution
                        execute_statement(statement, symbol_table, function_table, gui_print, gui_input)
                    executed_else_if = True
                    break
            
            if not executed_else_if: # NO WAI
                for statement in node.else_block:
                    execute_statement(statement, symbol_table, function_table, gui_print, gui_input)
    
    elif isinstance(node, SwitchNode): # WTF
        switch_value = lol_to_str(symbol_table.get("IT", "NOOB"))
        executed_case = False

        try: # check all cases
            for case in node.cases:
                if lol_to_str(case.literal_value) == switch_value:
                    for statement  in case.statements:
                        execute_statement(statement, symbol_table, function_table, gui_print, gui_input)
                    executed_case = True
                    break
            
            if not executed_case: # acts as the default case
                for statement in node.default_case:
                    execute_statement(statement, symbol_table, function_table, gui_print, gui_input)
        except BreakNode:
            pass

    elif isinstance(node, LoopNode): # loop / IM IN YR
        if node.var_name not in symbol_table:
            pass

        try: # loops until break is found (GTFO)
            while True:
                # loop condition
                if node.condition:
                    conditional_value = evaluate_expression(node.condition, symbol_table, function_table, gui_print, gui_input)
                    if node.condition_type == "WILE":
                        if not bool_convert(conditional_value):
                            break
                    elif node.condition_type == "TIL":
                        if bool_convert(conditional_value):
                            break
                
                # loop execution
                for statement in node.statements:
                    execute_statement(statement, symbol_table, function_table, gui_print, gui_input)

                # loop variable update
                current_value = lol_to_num(symbol_table[node.var_name])
                if node.operation == "UPPIN":
                    symbol_table[node.var_name] = current_value + 1
                elif node.operation == "NERFIN":
                    symbol_table[node.var_name] = current_value - 1
        except BreakNode:
            pass
    
    elif isinstance(node, BreakNode):
        raise BreakNode()

    elif isinstance(node, ReturnNode):
        return_value = evaluate_expression(node.expression, symbol_table, function_table, gui_print, gui_input)
        raise ReturnNode(return_value)
    
    elif isinstance(node, FunctionCallNode):
        result = evaluate_expression(node, symbol_table, function_table, gui_print, gui_input)
        symbol_table["IT"] = result
    
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
    
    elif isinstance(node, UnaryOpNode): # NOT
        value = evaluate_expression(node.operand, symbol_table, function_table, gui_print, gui_input)
        result = not bool_convert(value)
        return format_result(result)
    
    elif isinstance(node, InfiniteArityOpNode):
        operands = [evaluate_expression(op, symbol_table, function_table, gui_print, gui_input) for op in node.operands]

        if node.operator == "SMOOSH": # concat
            return "".join([lol_to_str(op) for op in operands])
        
        if node.operator == "ALL OF": # and
            result = all(bool_convert(op) for op in operands)
            return format_result(result)

        if node.operator == "ANY OF": # or
            result = any(bool_convert(op) for op in operands)
            return format_result(result)
        
    elif isinstance(node, FunctionCallNode): # I IZ
        function_definition = function_table.get(node.func_name)
        if not function_definition or len(node.arguments) != len(function_definition.parameters):
            pass # function not defined or other errors
        
        # evaluate argument in the top level scope
        argument_values = [evaluate_expression(argument, symbol_table, function_table, gui_print, gui_input) for argument in node.arguments]

        local_symbtable = {"IT": symbol_table.get("IT", "NOOB")} # define its own symbol table
        for parameters, argument_val in zip(function_definition.parameters, argument_values):
            local_symbtable[parameters] = argument_val

        # execution
        try:
            for statement in function_definition.statements:
                execute_statement(statement, local_symbtable, function_table, gui_print, gui_input)
        except ReturnNode as ret:
            return ret.value
    
        return "NOOB"

    elif isinstance(node, TypecastNode): # MAEK
        value = evaluate_expression(node.expression, symbol_table, function_table, gui_print, gui_input)
        target = node.target_type

        if target == "NUMBR":
            return int(lol_to_num(value))
        elif target == "NUMBAR":
            return float(lol_to_num(value))
        elif target == "YARN":
            return lol_to_str(value)
        elif target == "TROOF":
            if bool_convert(value):
                return "WIN"
            else:
                return "FAIL"
        elif target == "NOOB":
            return "NOOB"

    else:
        pass
        # print("Error")