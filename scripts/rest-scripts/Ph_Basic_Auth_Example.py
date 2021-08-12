import requests

# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()
r = requests.get('https://10.0.0.3/rest/container/1', auth=('basicuser', 'password123$'), verify=False)

print(r.content)
