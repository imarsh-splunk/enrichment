# Create Phantom container via REST POST
import requests
import json


def create_artifact(h, t):

    endpoint = '/rest/artifact'
    c_id = 97853
    a_name = 'POSTed Artifact'

    artifact_json = {
        "cef": {
            "key1": "val1"
        }
    }
    json_blob = json.dumps(artifact_json)

    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    r = requests.post('{}{}'.format(h, endpoint), data=json_blob, headers=headers, verify=False)
    return r


auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}

r = create_artifact(auth['server'], auth['ph-auth-token'])
print(r.content)
