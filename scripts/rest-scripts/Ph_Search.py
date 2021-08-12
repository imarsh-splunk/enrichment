import requests
import json

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

query = '175.111.5.112'

r = requests.get('https://{}/rest/search?query={}&page_size=0'.format(host, query), headers=headers, verify=False)

#r_json_pretty = json.dumps(r.json(), indent=1)

print(r.json())
