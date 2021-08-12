# Create Phantom container and add artifacts for each row item in an XLSX spreadsheet
import requests
import json
import pandas as pd

phantom_host = '172.16.101.130'
AUTH_TOKEN = 'dhq2JM5GP/SwW+5ClElihOj7v08lLPrLfWilLFAQNpM='
headers = {"ph-auth-token": "TOKEN_VALUE"}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

container_json = {
  "artifacts": [],
  "custom_fields": {},
  "data": {},
  "description": "Imported from PublicIPLists.xlsx email attachment",
  "label": "ip list import",
  "name": "Container created from PublicIPLists.xlsx via REST API",
  "run_automation": True,
  "sensitivity": "white",
  "severity": "low",
  "status": "new"
}
json_blob = json.dumps(container_json)
container_r = requests.post('https://{}/rest/container'.format(phantom_host), data=json_blob, headers=headers,
                            verify=False)

# print 'Container Creation Failed with error status code:{}'.format(container_r.status_code)

container_id = container_r.json()['id']

local_file = '/Users/cblumer/Documents/Ph_Testing_Data/PublicIPLists.xlsx'
df = pd.read_excel(local_file, sheet_name='ips')

for index, row in df.iterrows():
    artifact_json = {
        "cef": {
            "sourceAddress": "{}".format(row["Ip List "])
        },
        "container_id": container_id,
        "data": {},
        "label": "event",
        "run_automation": True,
        "severity": "low",
        "type": "network"}
    json_blob = json.dumps(artifact_json)
    artifact_r = requests.post('https://{}/rest/artifact'.format(phantom_host), data=json_blob, headers=headers,
                               verify=False)

    #print(artifact_r.status_code)
    print(artifact_r.content)
