import requests


host = '172.16.101.177'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
requests.packages.urllib3.disable_warnings()

r = requests.get('https://{}/rest/container_attachment?page_size=0'
                 .format(host), headers=headers, verify=False).json()['data']

for i in r:
    if ".eml" in i.get('name'):
        print(i)
