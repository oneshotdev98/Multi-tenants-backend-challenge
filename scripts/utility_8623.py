#!/usr/bin/env python3
# API helper functions
import requests

def fetch_data(url):
    """Fetch data from endpoint."""
    try:
        response = requests.get(url, timeout=5)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None
