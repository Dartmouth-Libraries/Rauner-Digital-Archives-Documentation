const REGULAR_FIELDS = new Set(['identifier', 'title']);
const DATE_FIELDS = new Set(['created', 'issued', 'modified', 'available']);
const PATTERN = /\<([A-Za-z]*)\>(.*)\<\/[A-Za-z]*\>/g;
const XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
// I am so naive for believing that 1 is actual 1 in this miserable world.
const ATTACHMENTS = input.config().attachments; // "input.config() can only be called once"
const TABLE = base.getTable("Test Table");

// Well I can loop through contentType and find `application/pdf` and `applicaton/octet-stream`
const OPEX_URL = ATTACHMENTS.find(a => a.contentType === "application/octet-stream")?.expiringDownloadUrl;
const PDF_URL = ATTACHMENTS.find(a => a.contentType === "application/pdf")?.expiringDownloadUrl;

if (!OPEX_URL || !PDF_URL) throw new Error("Faulty email. Please check log for more information");

main();

async function main() {

    const opex = await fetchOPEX(OPEX_URL)
                        // I need better error handling than this.
                        .catch(error => console.error(error));
    const metadata = extractXMLTags(opex, REGULAR_FIELDS);
    const date = findLatestDate(extractXMLTags(opex, DATE_FIELDS));

    metadata.date = date

    addRecords(TABLE, metadata)
}

async function fetchOPEX(url) {
    const response = await fetch(url);
    const contentType = response.headers.get("Content-Type");
    // it's supposed to be XML file but GMail considers it `octet-stream`
    const body = await response.text()
    if (!isOPEXFile(body, contentType)) throw new Error("Not an OPEX file!")
    return body
}

function isOPEXFile(file, contentType) {
    return contentType === "application/octet-stream"
                       && file.split(/\r?\n/)[0] === XML_DECLARATION
}

function extractXMLTags(text, tags) {
    const matches = text.matchAll(PATTERN);
    const values = {}
    for (const match of matches) {
        // By design, the second element in `match` is the tag's name,
        // and the third element is its text, or actual value.
        const tagName = match[1];
        const tagValue = match[2];
        if (tags.has(tagName)) values[tagName] = tagValue;
    }
    return values;
}

function findLatestDate(dates) {
    return Object.values(dates)
            .reduce((latest, current) => current > latest ? current : latest)
}

async function addRecords(table, metadata) {
    const recordID = await table.createRecordAsync({
            // I need to use more stable identifiers (i.e., field IDs).
            "Policy Code": metadata.identifier,
            "Policy Title": metadata.title,
            "Date": metadata.date,
            "Files": [
                {url: PDF_URL, filename: `${metadata.identifier}.pdf`},
                {url: OPEX_URL, filename: `${metadata.identifier}.pdf.opex`}
            ]
    })
    return recordID
}
