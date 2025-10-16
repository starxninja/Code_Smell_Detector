"""
File utility functions
"""

import os
from typing import Optional, List


def read_file(file_path: str) -> Optional[str]:
    """Read file content with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (IOError, OSError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def get_file_extension(file_path: str) -> str:
    """Get file extension"""
    return os.path.splitext(file_path)[1].lower()


def is_python_file(file_path: str) -> bool:
    """Check if file is a Python file"""
    return get_file_extension(file_path) == '.py'


def find_python_files(directory: str) -> List[str]:
    """Find all Python files in a directory recursively"""
    python_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if is_python_file(file):
                python_files.append(os.path.join(root, file))
    
    return python_files


def get_relative_path(file_path: str, base_path: str) -> str:
    """Get relative path from base path"""
    try:
        return os.path.relpath(file_path, base_path)
    except ValueError:
        return file_path
