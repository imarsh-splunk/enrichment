import requests

headers = {"ph-auth-token": 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

r = requests.get('https://10.0.0.3/rest/container/1', headers=headers, verify=False)

print(r.content)
