import requests
import json

auth = {
  "ph-auth-token": "WI+Gynyp/q7fbFrtGcBtzfZHr44yaBfKEkztdXcNvRo=",
  "server": "https://10.0.0.101"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

pid = 888
name = "100_geolocates_copy"

r = requests.get('{}/rest/playbook?_filter_name="{}"&page_size=0'.format(auth['server'], name),
                 headers=headers, verify=False).json()['data']
p_list = []

old_repo1 = "qascratchpad"
old_repo2 = "phinternal"

for i in r:
    pid = i['id']
    child_playbooks = i['metadata']['playbooks']
    if child_playbooks:
        p_list.append(child_playbooks)
# print(p_list)

for i, x in enumerate(p_list):
    for j, a in enumerate(x):
        p_list[i][j] = a.replace(old_repo1, 'local').replace(old_repo2, 'local')

new_p_list = p_list[0]
data = {"metadata": {"playbooks": new_p_list}}
print(data)

r = requests.post('{}/rest/playbook/{}'.format(auth['server'], pid),
                  data=json.dumps(data), headers=headers, verify=False)
print(r.content)

