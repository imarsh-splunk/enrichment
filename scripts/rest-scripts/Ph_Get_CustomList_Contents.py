import requests


def get_custom_list(h, t, i):

    ep = '/rest/decided_list/{}'.format(i)
    # formatted_content?_output_format=csv
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
list_id = 3

cl = get_custom_list(host, token, list_id)["content"]
print(cl)
