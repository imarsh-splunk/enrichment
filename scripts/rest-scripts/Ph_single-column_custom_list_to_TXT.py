# Create Phantom container via REST GET
import requests


def get_custom_list(h, t, list_id):

    ep = '/rest/decided_list/{}'.format(list_id)
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
custom_list_id = 1
custom_list = get_custom_list(host, token, custom_list_id)

txt = "/Users/cblumer/Documents/Ph_Testing_Data/EDL.txt"
with open(txt, 'w') as f:
    for item in custom_list['content']:
        item_str = item[0].encode('utf-8')
        f.write("{}\n".format(item_str))

txt = open(txt, "r").read()
print(txt)

