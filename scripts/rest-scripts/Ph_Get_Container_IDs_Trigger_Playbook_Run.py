import requests
import json
from datetime import datetime


def return_filtered_containers(ph_host, api, t, l, s):

    headers = {"ph-auth-token": api}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    try:
        endpoint = '/rest/container?_filter_label="{0}"&_filter_status="{1}"' \
                   '&_filter_create_time__gt="{2}"&page_size=0'.format(l, s, t)

        c = requests.get('https://{}{}'.format(ph_host, endpoint), headers=headers, verify=False)
        return c.json()['data']

    except TypeError as e:
        err = ('Error: {}'.format(e))
        return err


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='

today = datetime.now().strftime("%Y-%m-%d")
label = 'signalsciences'
status = 'new'
containers = return_filtered_containers(host, token, today, label, status)

c_ids = []

for item in containers:
    c_ids.append(item.get('id'))

print(c_ids)

pb_id = 'local/[HULU] - SignalSciences Playbook'

for c_id in c_ids:
    try:
        headers = {"ph-auth-token": token}
        # disable certificate warnings for self signed certificates
        requests.packages.urllib3.disable_warnings()

        run_playbook_json = {
            "container_id": c_id,
            "playbook_id": pb_id,
            "scope": "all",
            "run": True
        }
        json_blob = json.dumps(run_playbook_json)

        ep = '/rest/playbook_run'
        r = requests.post('https://{}{}'.format(host, ep), data=json_blob, headers=headers, verify=False)
        print(r.content)

    except TypeError as e:
        error = ('Error: {}'.format(e))
        print(error)
