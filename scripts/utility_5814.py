#!/usr/bin/env python3
# Data processing utility
import json

def load_config(path):
    """Load JSON configuration."""
    with open(path) as f:
        return json.load(f)

def validate_data(data):
    """Validate input data."""
    return all(isinstance(x, (int, str)) for x in data)
