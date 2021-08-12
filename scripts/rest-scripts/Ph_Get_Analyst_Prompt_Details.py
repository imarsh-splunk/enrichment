import requests
import json
import re
from ast import literal_eval

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = '38935'

pb_runs_ep = '/rest/action_run?_filter_container_id={}&_filter_action="prompt"&page_size=0'.format(cid)

r = requests.get('https://{}{}'.format(host, pb_runs_ep), headers=headers, verify=False).json()['data']
# print(r)

for i in r:
    print(i)
