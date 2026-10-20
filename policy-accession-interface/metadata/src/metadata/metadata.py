# I can't deal with the default xml.etree.ElementTree library.

import lxml.etree as ET
from lxml.builder import ElementMaker

# should I put this in the init file?
E = ElementMaker(namespace="http://www.openpreservationexchange.org/opex/v1.1",
                 nsmap={"opex": "http://www.openpreservationexchange.org/opex/v1.1"})

def main():
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
        backfilled = backfill_metadata(input_path, "2049-2019") # Not an actual acession number, just for testing.
        result = ET.tostring(
            backfilled,
            encoding="unicode",       # Returns a Python string, not bytes
            pretty_print=True,        # Formats with indents and line breaks
            xml_declaration=True      # Adds the XML header prefix
        )
        print(result)
    except ET.ParseError as e:
        print(e, file = sys.stderr)
        return 1

    new_file_name = input_path + ".fixed"
    backfilled.write(new_file_name,
                     xml_declaration = True,
                     standalone = True,
                     pretty_print = True,
                     encoding = "UTF-8")

def backfill_metadata(root: ET.Element, accession_number: str) -> ET.ElementTree:
    ns = {'dc': 'http://purl.org/dc/terms/'}

    code = root.findtext(".//dc:identifier", namespaces=ns)
    title = root.findtext(".//dc:title", namespaces=ns)

    # the type checker is freaking about these two being `None`
    assert code is not None and title is not None
    
    # this line of code is making me uncomfortable.
    dates = root.xpath(".//dc:created | .//dc:issued | .//dc:modified | .//dc:available",
                       namespaces=ns)

    for d in dates:
        print(type(d))

    # find the most recent date
    date = max([e.text for e in dates])
    description = f"{code}; {date}"

    root.append(
            E.Properties(
                E.Title(
                    title
                ),
                E.Identifiers(
                    E.Identifier(
                        accession_number
                    ),
                ),
                E.Description(
                    description
                )
            ))
    
    return root.getroottree()

if __name__ == "__main__":
    # Yes it's supposed to be imported on demand
    import os.path
    import sys

    sys.exit(main())
