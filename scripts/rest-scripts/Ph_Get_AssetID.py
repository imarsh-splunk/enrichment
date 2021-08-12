import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

name = 'maxmind'
r = requests.get('https://{}/rest/asset?_filter_name="{}"'.format(host, name), headers=headers, verify=False)
r_json_pretty = json.dumps(r.json()['data'], indent=1)
print(r_json_pretty)
