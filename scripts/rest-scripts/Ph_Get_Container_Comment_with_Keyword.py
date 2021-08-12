import requests
import json

auth = {
  "ph-auth-token": "tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8=",
  "server": "https://10.0.0.16"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 49491
keyword = 'LOOK_FOR_ME'

endpoint = '/rest/container/{}/comments?_filter_comment__contains="{}"'.format(cid, keyword)
r = requests.get('{}{}'.format(auth['server'], endpoint), headers=headers, verify=False).json()['data']

rjson = json.dumps(r, indent=1)
print(rjson)

