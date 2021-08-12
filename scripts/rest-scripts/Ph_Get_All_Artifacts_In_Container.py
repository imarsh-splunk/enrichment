import requests
from urlparse import urlparse
import urllib

host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

container_id = 1114
# name = "File Artifact"

r = requests.get('https://{}/rest/artifact?_filter_container_id={}&page_size=0'
                 .format(host, container_id), headers=headers, verify=False).json()['data']
print(r)

items = []

for i in r:
    # print(i)
    if i['name'] == "URL Artifact":
        items.append(i['cef']['requestURL'])

for i in items:
    icount = items.count(i)
    print(icount)


