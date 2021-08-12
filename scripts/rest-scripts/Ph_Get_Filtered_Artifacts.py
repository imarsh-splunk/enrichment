import requests

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

a_id = 328
cef_keys = ['requestURL', 'act']

endpoint = '/rest/artifact/{}?_filter_cef__in={}&page_size=0'.format(a_id, cef_keys)
r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()['cef']

print(r)
