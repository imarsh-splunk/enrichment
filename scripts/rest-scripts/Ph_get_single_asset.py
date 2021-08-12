import requests
import json

auth = {
  "ph-auth-token": "NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0=",
  "server": "https://172.16.133.128"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

assetid = 100


r = requests.get('{}/rest/asset/{}?page_size=0'.format(auth['server'], assetid), headers=headers, verify=False)
# print(r.content)

r_json_pretty = json.dumps(r.json(), indent=1)
print(r_json_pretty)

