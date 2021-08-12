import datetime
import requests
import json

# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
timestamp = datetime.datetime.now()

container_json = {
  "label": "report",
  "name": "SBUX Filehash Blacklist - {}".format(timestamp),
  "run_automation": False,
  "status": "New"}

container_r = requests.post('https://{}/rest/container'.format(host), data=json.dumps(container_json),
                            headers=headers, verify=False)
container_id = container_r.json()['id']

filename = 'blacklist500-1.txt'
file_path = '/Users/cblumer/Documents/Ph_Testing_Data/{}'.format(filename)

f = open(file_path, 'r').read().split('\n')

for line in f:
    artifact_json = {
        "cef": {
            "fileHash": "{}".format(line)
        },
        "container_id": container_id,
        "name": "Blocked Hash",
        "label": "filehash",
        "run_automation": False,
        "type": "network_report"}
    artifact_r = requests.post('https://{}/rest/artifact'.format(host), data=json.dumps(artifact_json),
                               headers=headers, verify=False)
    print (artifact_r.content)
