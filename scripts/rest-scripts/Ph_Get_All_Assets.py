import requests
import json

auth = {
  "ph-auth-token": "tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8=",
  "server": "https://10.0.0.16"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()


r = requests.get('{}/rest/asset?page_size=0'.format(auth['server']), headers=headers, verify=False)
r_json_pretty = json.dumps(r.json()['data'], indent=1)

print(r_json_pretty)

