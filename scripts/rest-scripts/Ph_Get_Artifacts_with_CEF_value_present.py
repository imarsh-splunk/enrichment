import requests

auth = {
  "ph-auth-token": "Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U=",
  "server": "https://10.0.0.125"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cef_key = 'destination_port'

endpoint = '/rest/artifact/?_filter_cef__{}__isnull=False&page_size=0'.format(cef_key)
r = requests.get('{}{}'.format(auth['server'], endpoint), headers=headers, verify=False).json()['data']
# print(r)

for i in r:
    # print(i)
    a_cef = i['cef']
    print(a_cef)
    cef_val = i['cef'].get(cef_key)
    # print(cef_val)
