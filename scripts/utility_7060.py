#!/usr/bin/env python3
# String utilities
def reverse_string(s):
    """Reverse a string."""
    return s[::-1]

def count_vowels(s):
    """Count vowels in string."""
    return sum(1 for c in s.lower() if c in 'aeiou')
