import requests
import json

# host = '10.0.0.3'
# token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
host = '172.16.101.151'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

ar_id = 2488
r = requests.get('https://{}/rest/app_run/{}?page_size=0'.format(host, ar_id),
                 headers=headers, verify=False).json()
rj = json.dumps(r, indent=1)

print(rj)
