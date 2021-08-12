# Get playbook run details
import requests
from datetime import datetime

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
    start = datetime.strptime(run['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    end = datetime.strptime(run['update_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    difference = end - start
    print(difference)
