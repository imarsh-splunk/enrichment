# Return Phantom Container by ID
import requests
import json

host = '10.0.0.16'
token = 'tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container/'
container_id = 108032

r = requests.get('https://{}{}{}'.format(host, endpoint, container_id),
                 headers=headers, verify=False).json()
c = json.dumps(r, indent=1)

print(c)
