import requests
import json
from datetime import datetime, timedelta

# host = '10.0.0.3'
# token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
host = '172.16.101.159'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 1304
daysago = 1
stime = (datetime.now() - timedelta(daysago)).strftime("%Y-%m-%d")
pb_runs_ep = '/rest/playbook_run?&_filter_container="{}"' \
             '&_filter_start_time__gt="{}"&page_size=0'.format(cid, stime)

r = requests.get('https://{}{}'.format(host, pb_runs_ep), headers=headers, verify=False)

pb_run_ids = []

for run in r.json()['data']:
    # runj = json.dumps(run, indent=1)
    # print(runj)
    pb_run_id = json.loads(run['message']).get('playbook_run_id')
    app_run_id = json.loads(run['message'])['result']
    arij = json.dumps(app_run_id, indent=1)
    # print(arij)
    # result = json.loads(run['message']).get('result')
    pb_run_ids.append([pb_run_id, app_run_id])

latest_pb_id = max(pb_run_ids)
print(latest_pb_id)


