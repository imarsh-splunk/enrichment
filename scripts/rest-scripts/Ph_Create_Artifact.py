# Create Phantom container via REST
import requests
import json


def create_artifact(h, t, c_id, a_name, auto):

    ep = '/rest/artifact'

    # Example cef fields. Can be modified as needed.
    artifact_json = {
        "cef": {
            "shortDescription": "Short Description from Phantom!",
            "description": "Description from Phantom!",
            "category": "Network",
            "primaryConfigurationItem": "b66ba9534f761300df6589dba310c716",
            "assignmentGroup": "Information Security",
            "caller": "8e826bf03710200044e0bfc8bcbe5d86",
            "location": "Colorado",
        },
            "name": a_name,
            "container_id": c_id,
            "label": "event",
            "run_automation": auto,
            "severity": "low",
            "type": "ticketing"
    }
    json_blob = json.dumps(artifact_json)

    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    r = requests.post('https://{}{}'.format(h, ep), data=json_blob, headers=headers, verify=False)
    return r.json()


host = 'xx.xx.xx.xx'
token = 'x'
container_id = 19
artifact_name = 'Artifact Name goes here'
run_automation = True

create = create_artifact(host, token, container_id, artifact_name, run_automation)
print(create)
