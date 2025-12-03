from lexer.lol_tokens import TokenType


class ASTNode: #base class for all AST nodes
    pass


class ProgramNode(ASTNode): #represents entire lolcode program
    def __init__(self, version=None): #initializes program with optional version number
        self.version = version
        self.statements = []


class VariableDeclNode(ASTNode): #represents variable declaration
    def __init__(self, var_name, initial_value=None): #stores variable name and optional initial value
        self.var_name = var_name
        self.initial_value = initial_value


class AssignmentNode(ASTNode): #represents variable assignment
    def __init__(self, var_name, expression): #stores target variable and value expression
        self.var_name = var_name
        self.expression = expression


class VisibleNode(ASTNode): #represents output statement
    def __init__(self, expressions): #stores list of expressions to output
        self.expressions = expressions


class GimmehNode(ASTNode): #represents input statement
    def __init__(self, var_name): #stores variable name to receive input
        self.var_name = var_name


class LiteralNode(ASTNode): #represents literal values
    def __init__(self, value, literal_type): #stores literal value and its type
        self.value = value
        self.literal_type = literal_type


class VariableNode(ASTNode): #represents variable reference
    def __init__(self, var_name): #stores variable name being referenced
        self.var_name = var_name


class BinaryOpNode(ASTNode): #represents binary arithmetic or boolean operation
    def __init__(self, operator, left, right): #initializes node with operator and two operands
        self.operator = operator
        self.left = left
        self.right = right


class UnaryOpNode(ASTNode): #represents unary operation
    def __init__(self, operator, operand): #stores operator and single operand
        self.operator = operator
        self.operand = operand


class InfiniteArityOpNode(ASTNode): #represents operations with unlimited operands
    def __init__(self, operator, operands): #stores operator and list of operands
        self.operator = operator
        self.operands = operands


class ComparisonNode(ASTNode): #represents comparison operation
    def __init__(self, operator, left, right): #stores comparison operator and operands
        self.operator = operator
        self.left = left
        self.right = right


class TypecastNode(ASTNode): #represents type casting operation
    def __init__(self, expression, target_type): #stores expression to cast and target type
        self.expression = expression
        self.target_type = target_type

class TypecastStatementNode(ASTNode):
    def __init__(self, var_name, target_type):
        self.var_name = var_name
        self.target_type = target_type   

class ConditionalNode(ASTNode): #represents if-else conditional structure
    def __init__(self): #initializes conditional with empty blocks
        self.if_block = []
        self.elif_blocks = []
        self.else_block = []


class ElifClauseNode(ASTNode): #represents else-if clause
    def __init__(self, condition): #stores condition expression and statements
        self.condition = condition
        self.statements = []


class SwitchNode(ASTNode): #represents switch-case structure
    def __init__(self): #initializes switch with empty cases
        self.cases = []
        self.default_case = []


class CaseNode(ASTNode): #represents single case in switch
    def __init__(self, literal_value): #stores case value and statements
        self.literal_value = literal_value
        self.statements = []


class LoopNode(ASTNode): #represents loop structure
    def __init__(self, label, operation, var_name): #initializes loop with label, operation type, and loop variable
        self.label = label
        self.operation = operation
        self.var_name = var_name
        self.condition = None
        self.condition_type = None
        self.statements = []


class FunctionDefNode(ASTNode): #represents function definition
    def __init__(self, func_name, parameters): #stores function name, parameters, and body
        self.func_name = func_name
        self.parameters = parameters
        self.statements = []


class FunctionCallNode(ASTNode): #represents function call
    def __init__(self, func_name, arguments): #stores function name and argument list
        self.func_name = func_name
        self.arguments = arguments


class ReturnNode(ASTNode): #represents return statement
    def __init__(self, expression): #stores return value expression
        self.expression = expression


class BreakNode(ASTNode): #represents break statement
    def __init__(self): #initializes break node
        pass