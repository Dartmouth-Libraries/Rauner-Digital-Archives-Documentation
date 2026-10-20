import json

import requests

url = "http://localhost:5000/api/v1/process-airtable-payload/tblObGsHeQIQIiTHv"

with open("example_payload.json") as f:
    json_payload = json.loads(f.read())

res = requests.post(url, json=json_payload)

print(res.status_code)
print(res.text)
