import requests
import json

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

query = '116.236.250.154'

r = requests.get('https://{}/rest/search?query={}&page_size=0'.format(phantom_host, query), headers=headers, verify=False)

r_json_pretty = json.dumps(r.json(), indent=1)

print r_json_pretty
