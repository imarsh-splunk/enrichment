import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/severity'

r = requests.get('https://{}{}'.format(host, endpoint),
                 headers=headers, verify=False).json()
c = json.dumps(r, indent=1)

print(c)
