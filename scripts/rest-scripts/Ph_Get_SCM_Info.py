import requests
import json

auth = {
  "ph-auth-token": "WI+Gynyp/q7fbFrtGcBtzfZHr44yaBfKEkztdXcNvRo=",
  "server": "https://10.0.0.101"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()


r = requests.get('{}/rest/scm?page_size=0'.format(auth['server']),
                 headers=headers, verify=False).json()['data']
rj = json.dumps(r, indent=1)
print(rj)

