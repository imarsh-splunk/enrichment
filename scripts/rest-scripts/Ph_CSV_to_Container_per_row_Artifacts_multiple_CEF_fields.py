# Create Phantom container from CSV file
# Add Artifacts to container for each row in CSV
# Add CEF fields to Artifacts for each value in row
# Upload CSV Report to Container's Vault
# Update Container to Run 'Active' Playbooks on Label
import datetime
import requests
import json
import pandas as pd
from base64 import b64encode

# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": AUTH_TOKEN}
timestamp = datetime.datetime.now()

container_json = {
  "label": "ip list import",
  "name": "PublicIPLists.csv Report - {}".format(timestamp),
  "run_automation": False,
  "status": "New"}

container_r = requests.post('https://{}/rest/container'.format(phantom_host), data=json.dumps(container_json),
                            headers=headers, verify=False)
print container_r.content
container_id = container_r.json()['id']

filename = 'PublicIPLists.csv'
file_path = '/Users/cblumer/Documents/Ph_Testing_Data/{}'.format(filename)
df = pd.read_csv(file_path)

for index, row in df.iterrows():
    artifact_json = {
        "cef": {
            "sourceAddress": "{}".format(row["Ip List "]),
            "zoneName": "{}".format(row["Zone "])  # Expand this dict to include as many row values as needed
        },
        "container_id": container_id,
        "name": "{}".format(row),
        "label": "reportRow",
        "run_automation": False,
        "type": "network_report"}
    artifact_r = requests.post('https://{}/rest/artifact'.format(phantom_host), data=json.dumps(artifact_json),
                               headers=headers, verify=False)
    print artifact_r.content

contents = open(file_path, 'rb').read()
serialized_contents = b64encode(contents)

attachment_json = {
  "container_id": container_id,
  "file_content": serialized_contents,
  "file_name": filename,
  "metadata": {
      "contains": [
          "vault id"
      ]
  }
}
attachment_r = requests.post('https://{}/rest/container_attachment'.format(phantom_host),
                             data=json.dumps(attachment_json), headers=headers, verify=False)
print attachment_r.content

updated_container_json = {
    "run_automation": True}

container_r = requests.post('https://{}/rest/container/{}'.format(phantom_host, container_id),
                            data=json.dumps(updated_container_json), headers=headers, verify=False)
print container_r.content
