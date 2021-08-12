import requests

host = '10.0.0.x'
token = 'xxxx14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/artifact?_filter_cef__payload__isnull=False&page_size=0'
r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()['data']

payloads = []

for i in r:
    payload = i.get('cef').pop('payload')
    payloads.append(payload)

print(payloads)
