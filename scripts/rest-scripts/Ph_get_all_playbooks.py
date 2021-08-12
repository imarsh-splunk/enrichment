# Get all playbooks
import requests
import json

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

r = requests.get('https://{}/rest/playbook'.format(host), headers=headers, verify=False)

r_pretty = json.dumps(r.json(), indent=1)
print(r_pretty)
