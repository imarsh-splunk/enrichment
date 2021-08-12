import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
# host = '172.16.101.177'
# token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

psize = 0
r = requests.get('https://{}/rest/artifact?page_size={}'
                 .format(host, psize), headers=headers, verify=False).json().get('data')

for a in r:
    # if a.get('container') == 1:
    print(a)
