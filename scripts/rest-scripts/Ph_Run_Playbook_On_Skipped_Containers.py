import requests
import json


host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

label = "suspicious_email_submission"
status = "new"

r = requests.get('https://{}/rest/container?_filter_label={}&page_size=0'
                 .format(host, status, label), headers=headers, verify=False)
containers = r.json().get('data')

cids = []

for container in containers:
    # print(container)
    c_id = container.get('id')
    cids.append(c_id)
print(cids)

pid = "local/PlayNameHere"  # replace with appropriate playbook name or ID

ep = '/rest/playbook_run'

for cid in cids:

    run_playbook_json = {
            "container_id": cid,
            "playbook_id": pid,
            "scope": "all",
            "run": True
        }

    json_blob = json.dumps(run_playbook_json)

    r = requests.post('https://{}{}'.format(host, ep), data=json_blob, headers=headers, verify=False)
    print(r.content)
