#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Miguel Jara Maldonado.
Creation Date: 2025-04-10.
Description: Interface for all system agents to ensure consistent structure.
"""

from fastmcp import FastMCP

mcp = FastMCP("CustomServer")


def _shift_text(text: str, shift: int) -> str:
    """Shift alphabetic characters while preserving case and other characters."""
    shifted_characters = []

    for character in text:
        if "a" <= character <= "z":
            shifted_characters.append(
                chr((ord(character) - ord("a") + shift) % 26 + ord("a"))
            )
        elif "A" <= character <= "Z":
            shifted_characters.append(
                chr((ord(character) - ord("A") + shift) % 26 + ord("A"))
            )
        else:
            shifted_characters.append(character)

    return "".join(shifted_characters)


@mcp.tool
def weird_sum(a: int, b: int) -> int:
    """
    Sums two numbers, but the second one is multiplied by two.

    Only use this tool when the user explicitly asks for the weird sum tool.
    """
    return a + (b * 2)


@mcp.tool
def greet(name: str) -> str:
    """Greet someone by his name."""
    return f"¡Hola, {name}! Este saludo vino de una herramienta MCP."


@mcp.tool
def encrypt_sentence(sentence: str) -> str:
    """Encrypt a sentence by shifting each letter three positions to the right."""
    return _shift_text(sentence, shift=3)


@mcp.tool
def decrypt_sentence(sentence: str) -> str:
    """Decrypt a sentence by shifting each letter three positions to the left."""
    return _shift_text(sentence, shift=-3)


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=4000)
