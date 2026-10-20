# Policy Accession Interface

## Content
The `airtable` folder contains scripts that runs as automation modules on Airtable.
The Airtable interface allows the user
to work with new policy portal accession requests in a centralized, shared space.
For the more technical details,
please see the documentation within the folder.

The `metadata` folder contains Python codes
of a [Flask]<https://flask.palletsprojects.com/en/stable/> application
that is intended to be run on a serverless platform
(e.g. Amazon Lambda and Google Cloud Run).
The server listens for requests with a JSON body,
which includes encoded PDF file and OPEX file,
and additional metadata entered by the user sent through Airtable automation.
When it receives such a request,
it will copy the presupplied Dublin Core metadata
into Preservica's own metadata format,
fill in the manually entered metadata,
and perform hashing for PDF files.
After the metadata has been properly processed,
and a manifest file is created accordingly,
the server will upload the files to a designated folder in
Dartmouth/Preservica's S3 "bucket" for ingest.

## Usage
The user will interact with a _Kanban_ style interface in Airtable.
The interface is automatically populated with policy files pending review,
for which the user can then enter or edit metadata necessary for the accession process.
The user can trigger automation
that sends completed entries to the `metadata` application to prepare the files for ingest
by clicking a button on the top right corner of the interface.
