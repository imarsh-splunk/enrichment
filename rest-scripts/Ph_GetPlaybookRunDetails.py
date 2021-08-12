# Return Phantom Container by ID
import requests
import json
import re

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

pb_runs_ep = '/rest/playbook_run?&page_size=0'

r1 = requests.get('https://{}{}'.format(phantom_host, pb_runs_ep),
                  headers=headers, verify=False)

for run in r1.json()['data']:
    print(run['playbook'])

pb_id = '241'
pb_ep = '/rest/playbook/{0}?&page_size=0'.format(pb_id)

# r2 = requests.get('https://{}{}'.format(phantom_host, pb_ep), headers=headers, verify=False)

# r_pretty = json.dumps(r2.json(), indent=1)
# print(r_pretty)


# pb_python = str(r2.json()['python'])
# regex = r"assets=(.*?),"
# assets = re.findall(regex, pb_python)
# print(assets)

