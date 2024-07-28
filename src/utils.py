import json
import re


def load_jsonc(filepath: str) -> str:
    with open(filepath) as f:
        file_contents = f.read()
        file_contents = re.sub(r"\/\/.*", "", file_contents)
        file_contents = re.sub(r"\/\*.*\*\/", "", file_contents, flags=re.DOTALL)
        return json.loads(file_contents)
