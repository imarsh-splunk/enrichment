import requests
import json

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()


endpoint = '/rest/system_settings'
r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()
r_pretty = json.dumps(r, indent=1)

print(r_pretty)


# debug_settings = r.get('debug_settings')
# print(debug_settings)
