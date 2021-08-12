# Return Phantom Container by ID
import requests
import json

auth = {
  "ph-auth-token": "JqbR8uDPcoZArlWZ7Q57BdtGq1z+/+Kdyr5KutZ8Grg=",
  "server": "https://10.0.0.80"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container/'
container_id = 1

r = requests.get('{}{}{}'.format(auth['server'], endpoint, container_id),
                 headers=headers, verify=False).json()
c = json.dumps(r, indent=1)

print(c)
