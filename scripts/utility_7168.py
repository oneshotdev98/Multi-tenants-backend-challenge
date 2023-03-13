#!/usr/bin/env python3
# Random utility script
import random

def process_data(items):
    """Process a list of items."""
    return [x * 2 for x in items]

if __name__ == "__main__":
    data = [random.randint(1, 100) for _ in range(10)]
    print(process_data(data))
