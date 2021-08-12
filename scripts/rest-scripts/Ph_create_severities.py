
import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

data = {
    "color": "yellow",
    "name": "medium",
    "is_default": True
}

endpoint = '/rest/severity'

r = requests.post('https://{}{}'.format(host, endpoint), data=json.dumps(data), headers=headers, verify=False)

print(r.content)
