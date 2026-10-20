from pathlib import Path
import argparse

# Take argument
# --path "./..dirname/" the directory to generate manifests for
# --object-number "archival_object_572877" this can take either the full name or just the number
# --archivesspace_url
# --preservica_url

parser = argparse.ArgumentParser(description = "Generate Manifest files for Preservica Ingest")
parser.add_argument("path")
parser.add_argument("-O", "--object_number")
parser.add_argument("-A", "--archivesspace-url")
# parser.add_argument("-P", "--prservica-url")

args = parser.parse_args()

path = Path(args.path)

print(type(path))

"""
Where do they want the object identifier? 
I can probably get rid of the silly aspace_obect wrapper.
If I can extract them from archive space?
At least for policy assession
"""

for node in iter_dir():
    generate_manifest()

# list subdirectories
def folder_manifest:
    return
