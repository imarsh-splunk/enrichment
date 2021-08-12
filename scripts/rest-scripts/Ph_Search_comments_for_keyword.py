import requests
import json

auth = {
  "ph-auth-token": "tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8=",
  "server": "https://10.0.0.16"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

keyword = 'LOOK_FOR_ME'
verbose = 'Container comment'

# endpoint = '/rest/search?query={}&page_size=0'.format(keyword)
endpoint = '/rest/search?query={}&categories=container&_filter_verbose="{}"&page_size=0'.format(keyword, verbose)
r = requests.get('{}{}'.format(auth['server'], endpoint), headers=headers, verify=False).json()['results']

rjson = json.dumps(r, indent=1)
print(rjson)

