import requests
import json
from datetime import datetime, timedelta

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 21
r = requests.get('https://{}/rest/app_run?_filter_container={}&page_size=0'.format(host, cid),
                 headers=headers, verify=False).json()

for item in r['data']:
    print(item)


