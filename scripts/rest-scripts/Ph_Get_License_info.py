import requests
import json

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

ep = '/rest/license'
r = requests.get('https://{}{}'.format(host, ep), headers=headers, verify=False)

rjson = json.dumps(r.json(), indent=1)


print(rjson)
