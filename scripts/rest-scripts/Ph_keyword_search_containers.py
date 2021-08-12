# Return Phantom Container by ID
import requests

phantom_host = '10.0.0.9'
AUTH_TOKEN = 'Bp1mGCiC/uaMaXTi0ZU3xpaWSQsa3PPZYUAXA5bb2dk='
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

value = 'Sumologic'

endpoint = '/rest/artifact'
filter_query = '?_filter_type__contains={}'.format(value)

r = requests.get('https://{}{}{}'.format(phantom_host, endpoint, filter_query),
                 headers=headers, verify=False)
r_dict = r.json()

print r_dict
