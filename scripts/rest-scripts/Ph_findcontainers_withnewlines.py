import requests

host = '10.0.0.254'
token = 'RJlbHl3UVESQVM3NfWmXYLAS1ylylpFT4ptOq1iFyIA='
param = 'closed'

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container?page_size=0'

r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()

cids = []

for i in r['data']:
    cid = i.get('id')
    cname = str(i.get('name'))
    if "\\r\\n" in cname:
        # print(cid, cname)
        cids.append(cid)

# cids_csv = ','.join([str(i) for i in cids])
cids_csv = ','.join(map(str, cids))

print(cids_csv)
