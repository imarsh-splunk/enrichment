# Create Phantom container via REST GET
import requests


def get_custom_list(h, t, i):

    ep = '/rest/decided_list/{}/formatted_content?_output_format=csv'.format(i)
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.content


phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
list_id = 1

cl = get_custom_list(host, token, list_id)
print(cl)

