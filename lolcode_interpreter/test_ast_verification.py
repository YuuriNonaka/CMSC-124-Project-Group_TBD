#!/usr/bin/env python3
"""
AST Building Verification Test
Tests whether the parser is actually constructing AST nodes
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer import tokenize_program
from parser import Parser, SyntaxError as LOLSyntaxError
from parser.ast_nodes import *

def test_basic_ast_creation():
    """Test if basic AST nodes are being created"""
    print("=" * 60)
    print("TEST 1: Basic AST Creation")
    print("=" * 60)
    
    code = """HAI
VISIBLE "hello"
KTHXBYE"""
    
    tokens = tokenize_program(code)
    parser = Parser(tokens)
    result = parser.parse()
    
    print(f"Parser result type: {type(result)}")
    print(f"Parser result: {result}")
    
    # Check if it's actually an AST node
    if isinstance(result, ProgramNode):
        print("✅ SUCCESS: Parser returned ProgramNode")
        print(f"   - Version: {result.version}")
        print(f"   - Statements: {len(result.statements)}")
        
        for i, stmt in enumerate(result.statements):
            print(f"   - Statement {i}: {type(stmt).__name__}")
            if isinstance(stmt, VisibleNode):
                print(f"     - Expressions: {len(stmt.expressions)}")
                for expr in stmt.expressions:
                    print(f"       - Expression: {type(expr).__name__} = {getattr(expr, 'value', 'N/A')}")
    else:
        print("❌ FAIL: Parser did not return ProgramNode")
        print(f"   Instead got: {type(result)}")

def test_variable_declaration_ast():
    """Test variable declaration AST nodes"""
    print("\n" + "=" * 60)
    print("TEST 2: Variable Declaration AST")
    print("=" * 60)
    
    code = """HAI
I HAS A x ITZ 5
KTHXBYE"""
    
    tokens = tokenize_program(code)
    parser = Parser(tokens)
    result = parser.parse()
    
    if isinstance(result, ProgramNode):
        print("✅ ProgramNode created")
        for i, stmt in enumerate(result.statements):
            print(f"   Statement {i}: {type(stmt).__name__}")
            if isinstance(stmt, VariableDeclNode):
                print(f"     - Variable: {stmt.var_name}")
                print(f"     - Initial value type: {type(stmt.initial_value)}")
                if stmt.initial_value:
                    print(f"     - Initial value: {stmt.initial_value.value}")
            else:
                print("❌ Expected VariableDeclNode but got different type")
    else:
        print("❌ No ProgramNode created")

def test_complex_ast():
    """Test more complex AST structure"""
    print("\n" + "=" * 60)
    print("TEST 3: Complex AST Structure")
    print("=" * 60)
    
    code = """HAI
I HAS A x ITZ 5
I HAS A y
VISIBLE SUM OF x AN 10
KTHXBYE"""
    
    tokens = tokenize_program(code)
    parser = Parser(tokens)
    result = parser.parse()
    
    if isinstance(result, ProgramNode):
        print("✅ ProgramNode created")
        print(f"Number of statements: {len(result.statements)}")
        
        for i, stmt in enumerate(result.statements):
            print(f"\nStatement {i}: {type(stmt).__name__}")
            
            if isinstance(stmt, VariableDeclNode):
                print(f"  Variable: {stmt.var_name}")
                if stmt.initial_value:
                    print(f"  Initial value: {stmt.initial_value.value} ({type(stmt.initial_value).__name__})")
                else:
                    print("  No initial value")
                    
            elif isinstance(stmt, VisibleNode):
                print(f"  Number of expressions: {len(stmt.expressions)}")
                for j, expr in enumerate(stmt.expressions):
                    print(f"    Expression {j}: {type(expr).__name__}")
                    if isinstance(expr, BinaryOpNode):
                        print(f"      Operator: {expr.operator}")
                        print(f"      Left: {type(expr.left).__name__} = {getattr(expr.left, 'var_name', getattr(expr.left, 'value', 'N/A'))}")
                        print(f"      Right: {type(expr.right).__name__} = {getattr(expr.right, 'value', 'N/A')}")
    else:
        print("❌ No ProgramNode created")

def test_ast_node_attributes():
    """Verify all AST nodes have expected attributes"""
    print("\n" + "=" * 60)
    print("TEST 4: AST Node Attributes Verification")
    print("=" * 60)
    
    code = """HAI
I HAS A name ITZ "Alice"
VISIBLE name
KTHXBYE"""
    
    tokens = tokenize_program(code)
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Check ProgramNode
    assert hasattr(ast, 'version'), "ProgramNode missing 'version' attribute"
    assert hasattr(ast, 'statements'), "ProgramNode missing 'statements' attribute"
    print("✅ ProgramNode attributes verified")
    
    # Check statements
    for i, stmt in enumerate(ast.statements):
        print(f"\nStatement {i}: {type(stmt).__name__}")
        
        if isinstance(stmt, VariableDeclNode):
            assert hasattr(stmt, 'var_name'), "VariableDeclNode missing 'var_name'"
            assert hasattr(stmt, 'initial_value'), "VariableDeclNode missing 'initial_value'"
            print(f"  ✅ VariableDeclNode: {stmt.var_name}")
            
        elif isinstance(stmt, VisibleNode):
            assert hasattr(stmt, 'expressions'), "VisibleNode missing 'expressions'"
            print(f"  ✅ VisibleNode with {len(stmt.expressions)} expressions")
            
            for expr in stmt.expressions:
                if isinstance(expr, VariableNode):
                    assert hasattr(expr, 'var_name'), "VariableNode missing 'var_name'"
                    print(f"    ✅ VariableNode: {expr.var_name}")
                elif isinstance(expr, LiteralNode):
                    assert hasattr(expr, 'value'), "LiteralNode missing 'value'"
                    assert hasattr(expr, 'literal_type'), "LiteralNode missing 'literal_type'"
                    print(f"    ✅ LiteralNode: {expr.value} ({expr.literal_type})")

def test_parser_return_value():
    """Check what the parser actually returns"""
    print("\n" + "=" * 60)
    print("TEST 5: Parser Return Value Analysis")
    print("=" * 60)
    
    # Simple test case
    code = "HAI\nKTHXBYE"
    
    tokens = tokenize_program(code)
    print(f"Tokens: {len(tokens)} tokens generated")
    
    parser = Parser(tokens)
    result = parser.parse()
    
    print(f"Parser.parse() returned: {result}")
    print(f"Return type: {type(result)}")
    print(f"Is it a ProgramNode? {isinstance(result, ProgramNode)}")
    print(f"Is it a bool? {isinstance(result, bool)}")
    print(f"Is it None? {result is None}")
    
    if hasattr(result, '__dict__'):
        print(f"Object attributes: {result.__dict__}")

def main():
    """Run all AST verification tests"""
    print("AST BUILDING VERIFICATION TESTS")
    print("This will check if your parser is actually constructing AST nodes")
    print()
    
    try:
        test_parser_return_value()
        test_basic_ast_creation()
        test_variable_declaration_ast()
        test_complex_ast()
        test_ast_node_attributes()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("If you see ProgramNode, VariableDeclNode, VisibleNode, etc.")
        print("above, then your AST building is WORKING CORRECTLY!")
        print()
        print("If you see only boolean True/False or None, then your parser")
        print("is only doing syntax validation without building AST nodes.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()