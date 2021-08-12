import requests
import json

phantom_host = '172.16.101.130'
AUTH_TOKEN = 'dhq2JM5GP/SwW+5ClElihOj7v08lLPrLfWilLFAQNpM='
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cef_field_L1 = 'emailHeaders'
cef_field_L2 = 'Subject'
query = 'Sumologic: Firewall Health Check Critical Alerts'

r = requests.get('https://{}/rest/artifact?_filter_cef__{}__{}="{}"'
                 .format(phantom_host, cef_field_L1, cef_field_L2, query), headers=headers, verify=False)

r_json_pretty = json.dumps(r.json(), indent=1)

print(r_json_pretty)
