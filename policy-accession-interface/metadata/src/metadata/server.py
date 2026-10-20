from base64 import b64decode
from datetime import datetime
from pathlib import Path
from typing import Literal

from flask import Flask, request
from lxml import etree as ET
from lxml.builder import ElementMaker

from ingest.metadata import backfill_metadata
from ingest.manifest import build_folder_manifest

app = Flask(__name__)

E = ElementMaker(namespace="http://www.openpreservationexchange.org/opex/v1.1",
                 nsmap={"opex": "http://www.openpreservationexchange.org/opex/v1.1"})

REQUIRED_FIELDS = ["collectionNumber",
                   "collectionTitle",
                   "accessionIdentifier",
                   "repository",
                   "policyDate",
                   "files"]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# it should return a stringified JSON object
@app.post("/api/v1/process-airtable-payload/<string:table_id>")
def test(table_id: str) -> tuple[dict, int]:
    data = request.json
    print(type(data))
    if not all(field in REQUIRED_FIELDS
               for field in data):
        return {"error": "Invalid or incomplete JSON object."}, 400

    try:
        encoded_pdf = data["files"]["encodedPDF"]
        encoded_opex = data["files"]["encodedOPEX"]
    except KeyError:
        return {"error": "Cannot find encoded file(s)."}, 400

    # extracting metadata
    accession_id: str = data["accessionIdentifier"]
    repository: Literal["Permanent", "Non-Permanent"] = data["repository"]
    collection_id: str = data["collectionNumber"]
    collection_title: str = data["collectionTitle"]

    # handling the actual file
    decoded_pdf = b64decode(encoded_pdf)
    decoded_opex = ET.fromstring(b64decode(encoded_opex)) # the root node of the decoded xml tree
    backfilled_opex = backfill_metadata(o, accession_id)
    print(ET.tostring(backfilled_opex, pretty_print=True, encoding=str))
    package_files(accession_id, backfilled_opex, decoded_pdf, collection_title, collection_id)
    return {"sucess": f"Uploaded to Amazon S3 at {datetime.now()}"}, 200

def package_files(accession_id: str,
                  opex: ET.ElementTree,
                  pdf: bytes,
                  # repository: Literal["Permanent", "Non-Permanent"],
                  collection_name: str,
                  collection_id: str):
    dir_path = Path(f"./{collection_id}-{collection_name}")
    dir_path.mkdir()
    opex.write(dir_path / "output.xml", 
               encoding="utf-8", 
               xml_declaration=True, 
               pretty_print=True)
    pdf_file_name = f"{accession_id}"
    with open(dir_path / (accession_id+".pdf"), "wb") as pdf_file:
          pdf_file.write(pdf)
    # For now let's ignore object ID
    manifest_tree = build_folder_manifest(dir_path, [], [pdf_file_name])
    print(ET.tostring(manifest_tree, pretty_print=True, encoding=str))
    opex.write(dir_path / (accession_id+".opex"), 
               encoding="utf-8", 
               xml_declaration=True, 
               pretty_print=True)
    print(str(dir_path))
    pass
