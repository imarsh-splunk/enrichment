import requests
import json


host = '10.0.0.254'
token = 'RJlbHl3UVESQVM3NfWmXYLAS1ylylpFT4ptOq1iFyIA='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 6615  # replace with appropriate container ID
pid = "local/domainEnrichment"  # replace with appropriate playbook name or ID

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
p_run_id = json.loads(r.content)['playbook_run_id']

r = requests.get('https://{}/rest/playbook_run/{}'.format(host, p_run_id), headers=headers, verify=False)
# print(r.content)

pb_status = r.get('status')

if pb_status == 'running':
    r = requests.get('https://{}/rest/playbook_run/{}'.format(host, p_run_id), headers=headers, verify=False)
else:
    # r_pretty = json.dumps(r.json(), indent=1)
    # print(r_pretty)
    print()