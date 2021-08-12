import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

container_id = 33
r = requests.get('https://{}/rest/system_settings'
                 .format(host, container_id), headers=headers, verify=False)

print(r.content)

