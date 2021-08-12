import requests
import json
from datetime import datetime, timedelta

host = '172.16.101.177'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

status = "running"
r = requests.get('https://{}/rest/app_run?_filter_status="{}"&page_size=0'.format(host, status),
                 headers=headers, verify=False).json()['data']

for i in r:
    print(i)
