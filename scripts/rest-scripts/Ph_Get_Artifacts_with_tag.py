import requests

host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

tag = 'email'

endpoint = '/rest/artifact/?_filter_tags__icontains="{}"&page_size=0'\
    .format(tag)
r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False)
# print(r.json()['data'])

for i in r.json()['data']:
    print(i)
