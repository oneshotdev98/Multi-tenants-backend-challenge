#!/usr/bin/env python3
# Math utilities
import math

def fibonacci(n):
    """Generate Fibonacci sequence."""
    if n <= 0:
        return []
    return [0] + [sum(fibonacci(n-1)[-2:]) for _ in range(n-1)]

def gcd(a, b):
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return a
