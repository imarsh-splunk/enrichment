# Return Phantom Container by ID
import requests

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
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
