# Create Phantom container via REST GET
import requests


def get_custom_list(h, t):

    ep = '/rest/decided_list'
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'

all_lists = get_custom_list(host, token)
for item in all_lists['data']:
    print(item)
