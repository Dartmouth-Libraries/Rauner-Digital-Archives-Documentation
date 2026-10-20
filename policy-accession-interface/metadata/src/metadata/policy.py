from lxml import etree as ET
from lxml.builder import ElementMaker
from ingest.manifest import calculate_fixity, 

E = ElementMaker(namespace="http://www.openpreservationexchange.org/opex/v1.1",
                 nsmap={"opex": "http://www.openpreservationexchange.org/opex/v1.1"})
def policy_manifest():
    return E.OPEXMetadata(
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
