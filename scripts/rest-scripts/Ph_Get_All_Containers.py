# Return all Phantom Containers
import requests
import json
import io

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
# host = '172.16.101.177'
# token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container?page_size=0'

r = requests.get('https://{}{}'.format(host, endpoint),
                 headers=headers, verify=False).json()

containers = json.dumps(r['data'], indent=1)
print(type(containers))
print(containers)

# with io.open('phantom_export.json', 'w', encoding='utf-8') as f:
    # f.write(json.dumps(r, ensure_ascii=False))

# print(outfile)
