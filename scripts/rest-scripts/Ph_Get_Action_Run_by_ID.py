import requests

auth = {
  "ph-auth-token": "NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0=",
  "server": "https://172.16.133.128"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

ar_id = 2493
r = requests.get('{}/rest/action_run/{}?page_size=0'.format(auth['server'], ar_id),
                 headers=headers, verify=False).json()

print(r)
