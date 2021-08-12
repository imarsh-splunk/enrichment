# Bulk close containers in a 'new' or 'open' status where a 'required on close' custom field is populated
import requests
import json

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

# 1 == 'new' AND 2 == 'open'
statuses = [1, 2]
custom_field_name = "custom_field_text"
endpoint = '/rest/container?_filter_status__in={}&_filter_custom_fields__{}__isnull=False&page_size=0'\
    .format(statuses, custom_field_name)

r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()['data']

cid_list = []
for i in r:
    cid = i.get('id')
    cid_list.append(cid)
    print(i)

for cid in cid_list:
    endpoint = '/rest/container/{}'.format(cid)
    post_data = {'status': 'closed'}
    payload = json.dumps(post_data)
    # print(payload)
    # r = requests.post('https://{}{}'.format(host, endpoint), data=payload, headers=headers, verify=False)
    # print(r.content)
