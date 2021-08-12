# Create Phantom container via REST GET
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

    req = requests.post('https://{}{}'.format(h, ep), data=json_blob, headers=head, verify=False)
    return req


host = 'phantom_ip_or_dns'
token = 'automation_user_api_token'
headers = {"ph-auth-token": token}

c_id = 1096 # replace with appropriate container ID
p_id = 'local/PlaybookName' # replace with appropriate playbook name or ID

r = run_playbook(host, token, c_id, p_id)
r_pretty = json.dumps(r.json(), indent=1)
p_run_id = json.loads(r.content)['playbook_run_id']
print(r_pretty)

r = requests.get('https://xx.xx.xx.xx/rest/playbook_run/{0}'.format(p_run_id), headers=headers, verify=False)
r_pretty = json.dumps(r.json(), indent=1)
print(r_pretty)
