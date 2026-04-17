#!/usr/bin/env python3
# File utilities
import os
import glob

def list_files(directory, pattern="*"):
    """List files in directory."""
    return glob.glob(os.path.join(directory, pattern))

def get_file_size(filepath):
    """Get file size in bytes."""
    return os.path.getsize(filepath)
