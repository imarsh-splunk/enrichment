import requests
import json

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

name = 'maxmind'
r = requests.get('https://{}/rest/asset?_filter_name="{}"'.format(phantom_host, name), headers=headers, verify=False)
r_json_pretty = json.dumps(r.json()['data'], indent=1)
print(r_json_pretty)
