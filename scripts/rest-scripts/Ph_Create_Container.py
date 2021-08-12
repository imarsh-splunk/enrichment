import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container'

container_json = {
  "asset_id": 1,
  "artifacts": [{
        "cef": {  # Add CEF fields here as needed
            "shortDescription": "Short Description from Phantom!",
            "description": "Description from Phantom!",
            "category": "Network",
            "primaryConfigurationItem": "b66ba9534f761300df6589dba310c716",
            "assignmentGroup": "Network Security",
            "caller": "8e826bf03710200044e0bfc8bcbe5d86",
            "location": "Colorado",
        },
        "name": "artifact_name",
        "label": "event",
        "run_automation": True,
        "severity": "low",
        "type": "rest_post"
    }],
  "custom_fields": {},
  "data": {},
  "description": "Useful description of this container dude",
  "label": "events",
  "name": "REST POST Container from External System",
  "run_automation": False,
  "sensitivity": "white",
  "severity": "low",
  "source_data_identifier": "client_name",
  "status": "new"}

json_blob = json.dumps(container_json)

container_r = requests.post('https://{}{}'.format(host, endpoint), data=json_blob, headers=headers, verify=False)

print(container_r.content)
