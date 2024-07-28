import os
import re


PARTS_PATTERN = r'{\s*(?:"[\w\d\s]+"\s*:\s*{\s*"baseStats"\s*:\s*{\s*"stitch"\s*:\s*[0-9]+,\s*"nerve"\s*:\s*[0-9]+,\s*"bone"\s*:\s*[0-9]+\s*},\s*"sockets"\s*:\s*{\s*"female"\s*:\s*[0-9]+,\s*"male"\s*:\s*[0-9]+\s*},\s*"slots"\s*:\s*[0-9]\s*},?\s*)*}'


def _validate(filepath: str, pattern: str) -> bool:

    with open(filepath) as f:
        file_contents = f.read()
        file_contents = re.sub(r"\/\/.*", "", file_contents)
        file_contents = re.sub(r"\/\*.*\*\/", "", file_contents, flags=re.DOTALL)
        return re.match(pattern, file_contents)


if __name__ == "__main__":

    if _validate(os.path.join(".", "data", "parts.jsonc"), PARTS_PATTERN):
        print("parts.jsonc Validated!")
    else:
        print("parts.jsonc Invalid!")
