import requests

auth = {
  "ph-auth-token": "NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0=",
  "server": "https://172.16.133.128"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cef_key = "sourceAddress"
endpoint = '/rest/container?_filter_artifact__cef__{}__isnull=False&page_size=0'.format(cef_key)

r = requests.get('{}{}'.format(auth['server'], endpoint), headers=headers, verify=False)
print(r.content)

for i in r.json()['data']:
    print(i)
