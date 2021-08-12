import requests
import json


def run_playbook(h, t, cid, pid):

    ep = '/rest/playbook_run'

    run_playbook_json = {
        "container_id": cid,
        "playbook_id": pid,
        "scope": "all",
        "run": True
    }
    json_blob = json.dumps(run_playbook_json)

    head = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    req = requests.post('https://{}{}'.format(h, ep), json=json_blob, headers=head, verify=False)
    return req


host = '10.0.0.254'
token = 'RJlbHl3UVESQVM3NfWmXYLAS1ylylpFT4ptOq1iFyIA='
headers = {"ph-auth-token": token}

c_id = 412  # replace with appropriate container ID
p_id = 'local/investigate'  # replace with appropriate playbook name or ID

r = run_playbook(host, token, c_id, p_id)
# r_pretty = json.dumps(r.json(), indent=1)
# p_run_id = json.loads(r.content)['playbook_run_id']
# print(r_pretty)

# r = requests.get('https://{}/rest/playbook_run/{}'.format(host, p_run_id), headers=headers, verify=False)
# r_pretty = json.dumps(r.json(), indent=1)
print(r)
