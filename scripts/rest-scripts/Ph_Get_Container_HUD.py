# Return HUD data from particular container
import requests
import json

phantom_host = '172.16.101.130'
AUTH_TOKEN = 'dhq2JM5GP/SwW+5ClElihOj7v08lLPrLfWilLFAQNpM='
#phantom_host = '10.0.0.9'
#AUTH_TOKEN = 'Bp1mGCiC/uaMaXTi0ZU3xpaWSQsa3PPZYUAXA5bb2dk='
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container_pin'
container_id = '1104'

r = requests.get('https://{}{}?_filter_container={}&page=0'.format(phantom_host, endpoint, container_id),
                 headers=headers, verify=False)
r_json_pretty = json.dumps(r.json(), indent=1)
print(r_json_pretty)

