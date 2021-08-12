import requests
import json
import ioc_fanger

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

container_id = '1069'
r = requests.get('https://{}/rest/artifact?_filter_container_id={}&page_size=0'.format(phantom_host, container_id),
                 headers=headers, verify=False)

r_json_pretty = json.dumps(r.json(), indent=1)

sourceAddress_fields = []
zoneName_fields = []

for artifact in r.json()['data']:
    sourceAddress_fields.append(str(artifact['cef']['sourceAddress']))
    zoneName_fields.append(str(artifact['cef']['zoneName']))

for ip in sourceAddress_fields:
    fanged_IP = ioc_fanger.defang(ip)
    print fanged_IP

# print r_json_pretty
print sourceAddress_fields
# print zoneName_fields
