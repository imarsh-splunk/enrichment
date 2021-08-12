import requests
import json

auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container'

container_json = {
  "asset_id": 1,
  "artifacts": [
    {"name": "IP Artifact",
        "cef": {
            "sourceAddress": "127.0.0.3"
        }
    },
    {"name": "IP Artifact",
        "cef": {
            "sourceAddress": "127.0.0.4"
        }
    },
    {"name": "Hash Artifact",
        "cef": {
            "fileHash": "0123456789abcdef0123456789abcdef"
        }
    },
    {"name": "Hash Artifact",
        "cef": {
            "fileHash": "abcdef0123456789abcdef0123456789"
        }
    }
  ],
  "custom_fields": {},
  "data": {},
  "description": "Useful description of this container dude",
  "label": "events",
  "name": "REST POST Container from External System",
  "run_automation": False,
  "sensitivity": "white",
  "severity": "low",
  "source_data_identifier": "GUID2",
  "status": "new"}

json_blob = json.dumps(container_json)

container_r = requests.post('{}{}'.format(auth['server'], endpoint), data=json_blob, headers=headers, verify=False)

print(container_r.content)
