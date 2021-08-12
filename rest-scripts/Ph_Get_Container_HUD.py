# Return HUD data from particular container
import requests
import json

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container_pin'
container_id = '1104'

r = requests.get('https://{}{}?_filter_container={}&page=0'.format(phantom_host, endpoint, container_id),
                 headers=headers, verify=False)
r_json_pretty = json.dumps(r.json(), indent=1)
print(r_json_pretty)

