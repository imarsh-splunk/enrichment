import requests
import json
import re
from ast import literal_eval

# host = '10.0.0.3'
# token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
host = '172.16.101.148'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

pb_runs_ep = '/rest/playbook_run?&_filter_start_time__gt="2019-02-09"&page_size=0'

r = requests.get('https://{}{}'.format(host, pb_runs_ep), headers=headers, verify=False)

for run in r.json()['data']:
    time = run['start_time']
    playbook = run['playbook']
    msg = run['message']
    pb_run_id = json.loads(msg).get('name')
    print([time, playbook, pb_run_id])
    #print(type(msg))
    #print(msg)
    print(pb_run_id)

    # status = run['status']
    # time = run['start_time']
    # playbook_id = run['id']
    # message = run['message']
    # print(message)
    # print([status, time, playbook_id, message])



    # if status == 'failed':
        # playbook_id = run['id']
        # container_id = run['container']
        # message = run['message']
        # print(playbook_id, container_id, message)

#pb_id = '241'

#pb_ep = '/rest/playbook/{0}?&page_size=0'.format(pb_id)





# r2 = requests.get('https://{}{}'.format(phantom_host, pb_ep), headers=headers, verify=False)

# r_pretty = json.dumps(r2.json(), indent=1)
# print(r_pretty)


# pb_python = str(r2.json()['python'])
# regex = r"assets=(.*?),"
# assets = re.findall(regex, pb_python)
# print(assets)

