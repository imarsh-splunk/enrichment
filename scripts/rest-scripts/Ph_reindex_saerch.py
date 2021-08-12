import requests
import json


host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

ep = '/rest/system_settings'

payload = {"reindex_section": True, "reindex_select": "actionrun"}
# payload = {"reindex_section": True, "reindex_select": "app"}
# payload = {"reindex_section": True, "reindex_select": "artifact"}
# payload = {"reindex_section": True, "reindex_select": "container"}
# payload = {"reindex_section": True, "reindex_select": "docs"}
# payload = {"reindex_section": True, "reindex_select": "playbook"}

r = requests.post('https://{}{}'.format(host, ep), data=json.dumps(payload), headers=headers, verify=False)
print(r.content)
