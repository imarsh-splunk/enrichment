# Bulk close containers in a 'new' or 'open' status where a 'required on close' custom field is populated
import requests
import json

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()


endpoint = '/rest/container'
r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()['data']

cid_list = []
for i in r:
    cid = i.get('id')
    cid_list.append(cid)
    # print(cid)

for cid in cid_list:
    endpoint = '/rest/container/34368/audit'.format(cid)
    r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False)
    print(r.content)

