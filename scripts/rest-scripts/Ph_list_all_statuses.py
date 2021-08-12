import requests
import json


auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container_status'

r = requests.get('{}{}'.format(auth['server'], endpoint),
                 headers=headers, verify=False).json().get('data')
# c = json.dumps(r, indent=1)

open_new = []
resolved = []
for i in r:
    if i['status_type'] in ['open', 'new']:
        open_new.append(i['id'])
    elif i['status_type'] == 'resolved':
        resolved.append(i['id'])

print(open_new)
print(resolved)


new_status_ids = [i['status_type'] for i in r]

# print(new_status_ids)
