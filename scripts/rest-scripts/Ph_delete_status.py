
import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

status_id = 13
endpoint = '/rest/container_status/{}'.format(status_id)

r = requests.delete('https://{}{}'.format(host, endpoint), headers=headers, verify=False)

print(r.content)
