# Increment an integer CEF field value within an Artifact
import requests
import json
import re

host = '172.16.101.177'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

aid = 5067
ep = '/rest/artifact/{}'.format(aid)
artifact = requests.get('https://{}{}'.format(host, ep), headers=headers, verify=False).json()
# print(artifact)

key = 'act'
new_val = 'updated_tothis_value'
artifact['cef'][key] = new_val

artifact = json.dumps(artifact)
clean_artifact = artifact.replace('null', '""').replace('false', '"False"').replace('true', '"True"')
# print(clean_artifact)

r = requests.post('https://{}{}'.format(host, ep), data=clean_artifact, headers=headers, verify=False)
print(r.content)
