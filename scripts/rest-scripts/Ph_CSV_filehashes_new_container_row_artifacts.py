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

phantom_host = '172.16.101.130'
AUTH_TOKEN = 'dhq2JM5GP/SwW+5ClElihOj7v08lLPrLfWilLFAQNpM='
headers = {"ph-auth-token": AUTH_TOKEN}
timestamp = datetime.datetime.now()

container_json = {
  "label": "cylance block hash",
  "name": "Cylance Bulk FileHash Block List - {}".format(timestamp),
  "run_automation": False,
  "status": "New"}

container_r = requests.post('https://{}/rest/container'.format(phantom_host), data=json.dumps(container_json),
                            headers=headers, verify=False)
# print (container_r.content)
container_id = container_r.json()['id']

filename = 'SWIFT_hashes.csv'
file_path = '/Users/cblumer/Documents/Ph_Testing_Data/{}'.format(filename)
df = pd.read_csv(file_path)

for index, row in df.iterrows():
    artifact_json = {
        "cef": {
            "fileHash": "{}".format(row[0])
        },
        "container_id": container_id,
        "name": "{}".format(row[0]),
        "label": "filehash",
        "run_automation": False,
        "type": "network_report"}
    artifact_r = requests.post('https://{}/rest/artifact'.format(phantom_host), data=json.dumps(artifact_json),
                               headers=headers, verify=False)

    s = requests.session()
    s.config['keep_alive'] = False

    # print (artifact_r.content)

updated_container_json = {
    "run_automation": True}

container_r = requests.post('https://{}/rest/container/{}'.format(phantom_host, container_id),
                            data=json.dumps(updated_container_json), headers=headers, verify=False)
# print (container_r.content)
