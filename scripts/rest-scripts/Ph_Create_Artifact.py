# Create Phantom container via REST POST
import requests
import json


def create_artifact(h, t):

    endpoint = '/rest/artifact'
    c_id = 2209
    a_name = 'POSTed Artifact'

    artifact_json = {
        "cef": {
            "shortDescription": "Short Description from Phantom!",
            "description": "Description from Phantom!",
            "category": "Network",
            "primaryConfigurationItem": "b66ba9534f761300df6589dba310c716",
            "assignmentGroup": "Network Security",
            "caller": "8e826bf03710200044e0bfc8bcbe5d86",
            "location": "Colorado",
        },
        "name": a_name,
        "container_id": c_id,
        "label": "event",
        "run_automation": False,
        "severity": "low",
        "type": "ticketing"
    }
    json_blob = json.dumps(artifact_json)

    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    r = requests.post('https://{}{}'.format(h, endpoint), data=json_blob, headers=headers, verify=False)
    return r


host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='

r = create_artifact(host, token)
print(r.content)
