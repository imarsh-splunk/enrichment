# Return all Phantom Containers
import requests
import json
import io

host = '172.16.101.177'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/ping'

r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False)

# print(type(r.content))
print(r.content)

