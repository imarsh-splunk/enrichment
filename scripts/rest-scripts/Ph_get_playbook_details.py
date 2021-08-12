# Get playbook details
import requests
import json
import re

auth = {
  "ph-auth-token": "tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8=",
  "server": "https://10.0.0.16"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

pb_runs_ep = '/rest/playbook_run?&page_size=0'

r1 = requests.get('{}{}'.format(auth['server'], pb_runs_ep),
                  headers=headers, verify=False)

for run in r1.json()['data']:
    print(run)

pb_id = '241'
pb_ep = '/rest/playbook/{0}?&page_size=0'.format(pb_id)

# r2 = requests.get('https://{}{}'.format(phantom_host, pb_ep), headers=headers, verify=False)

# r_pretty = json.dumps(r2.json(), indent=1)
# print(r_pretty)


# pb_python = str(r2.json()['python'])
# regex = r"assets=(.*?),"
# assets = re.findall(regex, pb_python)
# print(assets)

