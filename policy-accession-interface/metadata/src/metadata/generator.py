import argparse
import os
from pathlib import Path
from urllib.parse import urlsplit

import lxml.etree as ET

from ingest.manifest import build_folder_manifest

# Take argument
# --path "./..dirname/" the directory to generate manifests for
# --object-number "archival_object_572877" this can take either the full name or just the number
# --archivesspace_url
# --preservica_url

parser = argparse.ArgumentParser(description = "Generate Manifest files for Preservica Ingest")

parser.add_argument("path")

aspace_args = parser.add_mutually_exclusive_group()
aspace_args.add_argument("-O", "--object-number", type=str, default=None)
aspace_args.add_argument("-A", "--archivesspace-url", type=str)

parsed = parser.parse_args()

# There must be a more elegant way to write this.
# How can I be so oblivious to the best practices

if parsed.archivesspace_url:
    # should i turn this into a function?
    aspace_id =  (urlsplit(parsed.archivesspace_url)
                  .fragment
                  # .fragment returns a bytes-like object for some reason.
                  .decode('utf-8')
                  .split('::')[1])
elif parsed.object_number:
    aspace_id = "archival_object_" + parsed.object_number

# this program does not support relative path for some reason?????? 
# And it has problem with trailing slash?????
# Why so many problems aaaaaaaahhhhh
# This is the most stupid code I've written, period.
path = Path(parsed.path if os.name != "nt"
            # This is my call for ending all Windows atrocities
            else parsed.path.removesuffix('"'))

print(str(path))

# Where do they want the object identifier? 
# I can probably get rid of the silly aspace_obect wrapper.
# If I can extract them from archive space?
# At least for policy accession

for i, (current, folders, files) in enumerate(path.walk()):
    if i == 0 and parsed.object_number:
        manifest = (build_folder_manifest(current,
                                          folders,
                                          files,
                                          aspace_id)) # Is it okay to pass None here?
    else:
        manifest = build_folder_manifest(current, folders, files)
    text = ET.tostring(manifest,
                       encoding="UTF-8",
                       xml_declaration=True,
                       pretty_print=True,
                       standalone=True)
    # Holy grail for overloading the division operator
    with open(current / f"{current.name}.opex", "wb") as f:
        f.write(text)
