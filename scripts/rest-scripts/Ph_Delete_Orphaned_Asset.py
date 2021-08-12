import requests
import json

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

name = 'bigquery'
get_r = requests.get('https://{}/rest/asset?_filter_name="{}"'.format(host, name), headers=headers, verify=False)
# r_json_pretty = json.dumps(get_r.json()['data'], indent=1)

asset_id = get_r.json()['data'][0].get('id')
del_r = requests.delete('https://{}/rest/asset/{}'.format(host, asset_id), headers=headers, verify=False)

print(del_r.json())
