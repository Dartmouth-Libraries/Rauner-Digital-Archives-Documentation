from .metadata import backfill_metadata

import sys
import os.path

def main() -> int:
    if not sys.argv[1]:
        print("You did not provide a file path. Please check your input")
        return 2
    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print("The linked file does not exist. Please check your input.")
        return 67
    if os.path.splitext(input_path)[1] != ".opex":
        print("The input file is not an .opex file. Please check your input") 
        return 65

    try:
        backfilled = backfill_metadata(input_path, "2049-2019")
        print(backfilled)
    except Exception as e:
        print(e, file = sys.stderr)
        return 1

    new_file_name = input_path + ".fixed"
    backfilled.write(new_file_name)
    return 0
