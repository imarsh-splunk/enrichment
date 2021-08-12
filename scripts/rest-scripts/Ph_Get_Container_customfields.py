import requests
import json

auth = {
  "ph-auth-token": "Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U=",
  "server": "https://10.0.0.125"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container/'
container_id = 164038

r = requests.get('{}{}{}'.format(auth['server'], endpoint, container_id),
                 headers=headers, verify=False).json()
# print(r)

rstr = json.dumps(r, indent=1)
# print(rstr)

all_custom_fields = r['custom_fields']
print(all_custom_fields)

fieldkey = 'custom_field_text'
fieldval = r['custom_fields'].get(fieldkey)
# print(fieldval)
