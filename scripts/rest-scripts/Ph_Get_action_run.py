import requests

auth = {
  "ph-auth-token": "NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0=",
  "server": "https://172.16.133.128"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 21
r = requests.get('{}/rest/app_run?_filter_container={}&page_size=0'.format(auth['server'], cid),
                 headers=headers, verify=False).json()

for item in r['data']:
    print(item)
    app_run_id = item['action_run']
    print(app_run_id)
