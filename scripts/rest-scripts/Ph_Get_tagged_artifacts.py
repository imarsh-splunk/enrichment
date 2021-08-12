import requests

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

tag = 'WAF_BLOCK_ACTIVE'
ep = '/rest/artifact?_filter_tags__contains="{}"&page_size=0'.format(tag)

r = requests.get('https://{}{}'.format(host, ep), headers=headers, verify=False).json()['data']
# print(r)

for i in r:
    print(i)

