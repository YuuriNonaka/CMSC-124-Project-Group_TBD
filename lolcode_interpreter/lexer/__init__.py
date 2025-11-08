#lexer/__init__.py

from .lexer import tokenize_program
from .lol_tokens import TokenType

__all__ = ["tokenize_program", "TokenType"]
