import requests
import json


host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 1051  # replace with appropriate container ID
pid = 730  # replace with appropriate playbook name or ID

ep = '/rest/playbook_run'

run_playbook_json = {
        "container_id": cid,
        "playbook_id": pid,
        "scope": "all",
        "run": True
    }

json_blob = json.dumps(run_playbook_json)

r = requests.post('https://{}{}'.format(host, ep), data=json_blob, headers=headers, verify=False)
print(r.content)
