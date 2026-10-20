import boto3
from botocore.exceptions import ClientError

client = boto3.client('s3')

with open("C://Users/f007b70/Desktop/ingest/test/text.opex", "rb") as f:
    response = client.upload_fileobj(f, "bulk", "opex-policy/test.opex")
