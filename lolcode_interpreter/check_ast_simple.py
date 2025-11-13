#!/usr/bin/env python3
"""
Quick AST Diagnostic Check
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lexer import tokenize_program
from parser import Parser

# Test with simplest possible code
code = "HAI\nKTHXBYE"

print("Testing with code:")
print(code)
print()

tokens = tokenize_program(code)
print(f"Generated {len(tokens)} tokens")

parser = Parser(tokens)
result = parser.parse()

print(f"\nParser result: {result}")
print(f"Result type: {type(result)}")

if hasattr(result, '__dict__'):
    print(f"Result attributes: {result.__dict__}")
else:
    print("Result has no attributes (might be primitive type)")

# Check if it's an AST node
try:
    from parser.ast_nodes import ProgramNode
    if isinstance(result, ProgramNode):
        print("✅ SUCCESS: Parser is building AST nodes!")
        print(f"   - Version: {result.version}")
        print(f"   - Statements: {len(result.statements)}")
    else:
        print("❌ Parser is NOT building AST nodes - it's returning something else")
except ImportError:
    print("⚠️  Could not import AST node classes")