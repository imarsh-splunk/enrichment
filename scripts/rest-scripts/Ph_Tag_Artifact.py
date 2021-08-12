import requests
import json

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

a_id = 474855
endpoint = '/rest/artifact/{}'.format(a_id)

post_data = {
    "tags": ["WAF_BLOCK_ACTIVE", "signal_sciences"]
}

json_blob = json.dumps(post_data)

r = requests.post('https://{}{}'.format(host, endpoint), data=json_blob, headers=headers, verify=False)
print(r.content)
