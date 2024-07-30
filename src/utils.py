"""
Utilities.

Various util functions used throughout the codebase.
"""

import json
import re


def load_jsonc(filepath: str) -> dict:
    """Return a dict as parsed from a json or jsonc file."""
    with open(filepath) as f:
        file_contents = f.read()
        file_contents = re.sub(r"\/\/.*", "", file_contents)
        file_contents = re.sub(r"\/\*.*\*\/", "", file_contents, flags=re.DOTALL)
        return json.loads(file_contents)
