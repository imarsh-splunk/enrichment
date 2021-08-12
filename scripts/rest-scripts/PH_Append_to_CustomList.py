import requests
import time
import json


timeOfaddition= int(time.time())
new_row = ['123.123.123.123', 'BR', timeOfaddition]

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

list_id = 6
ep = '/rest/decided_list/{}'.format(list_id)

append = {"append_rows": [new_row]}
json_blob = json.dumps(append)

r = requests.post('https://{}{}'.format(host, ep), data=json_blob, headers=headers, verify=False)
print(r.json())
