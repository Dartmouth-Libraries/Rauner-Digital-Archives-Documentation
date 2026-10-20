from hashlib import sha1
from pathlib import Path, PurePath

from lxml import etree as ET
from lxml.builder import ElementMaker

E = ElementMaker(namespace="http://www.openpreservationexchange.org/opex/v1.1",
                 nsmap={"opex": "http://www.openpreservationexchange.org/opex/v1.1"})

def build_folder_manifest(current_dir: Path,
                          folder_names: list[str],
                          file_names: list[str],
                          object_id: str | None = None) -> ET.ElementTree:

    folder_manifest = E.OPEXMetadata(
                            E.Transfer(
                                E.Fixities(
                                    *fill_fixities(current_dir)
                                ),
                                E.Manifest(
                                    *generate_manifest(folder_names, file_names)
                                )
                            ),
                            E.Properties(
                                E.Title(
                                    current_dir.name
                                ),
                                # Conditionally insert object_id
                                (
                                    E.Identifiers(
                                        E.Identiifer(
                                            object_id,
                                            type="Code"
                                            )
                                        ) if object_id else {}
                                )
                            ),
                            # I don't why they exist???
                            # E.DescriptiveMetadata(
                            #     E.LegacyXIP(
                            #         
                            #     )
                            # )
                        ).getroottree()
    return folder_manifest

# maybe there's a more elegant way to write this function
# recursive search for files and directory should be done in  
def enumerate_nodes(current_dir: Path) -> tuple[list[str], list[str]]:  
    file_names = [node.name for node in current_dir.iterdir() if node.is_file()]
    folders_names = [node.name for node in current_dir.iterdir() if node.is_dir()]
    return file_names, folders_names

def generate_manifest(folder_names: list[str],
                      file_names: list[str]) -> tuple[ET.Element, ET.Element]:
    files = E.Files(*[E.File(name) for name in file_names])
    folders = E.Folders(*[E.Folder(name) for name in folder_names])

    return files, folders

def fill_fixities(current_dir: Path) -> list[ET.Element]:
    # Should I use list comprehension here?
    fixity_tags = []
    for path in current_dir.iterdir():
        # we only want NON-OPEX files, so bye bye folders.
        if path.is_dir() or path.suffix == ".opex":
            continue
        # For each fixity tag,
        # we need "path", "type", "value"
        file_fixity = E.Fixity(calculate_fixity(path), # value is sandwiched between the opening and the closing tag
                               path=path.name,
                               type="SHA1") 
        fixity_tags.append(file_fixity)
    return fixity_tags

def calculate_fixity(path: Path) -> str:
    raw = path.read_bytes()
    checksum = sha1(raw).hexdigest()
    return checksum
