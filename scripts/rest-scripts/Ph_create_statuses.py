
import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

data = {
    "name": "new",
    "status_type": "new",
    "is_default": True
}

endpoint = '/rest/container_status'

r = requests.post('https://{}{}'.format(host, endpoint), data=json.dumps(data), headers=headers, verify=False)

print(r.content)
