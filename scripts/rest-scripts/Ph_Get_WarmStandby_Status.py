import requests
import json

auth = {
  "ph-auth-token": "WI+Gynyp/q7fbFrtGcBtzfZHr44yaBfKEkztdXcNvRo=",
  "server": "https://10.0.0.101"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

name = "100_geolocates_copy"

r = requests.get('{}/rest/playbook?_filter_name="{}"&page_size=0'.format(auth['server'], name),
                 headers=headers, verify=False).json()['data']
# rj = json.dumps(r, indent=1)
# print(rj)

for i in r:
    print(i)