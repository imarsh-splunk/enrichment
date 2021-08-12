import requests
import json
import urllib

auth = {
  "ph-auth-token": "NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0=",
  "server": "https://172.16.133.128"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

action = 'url reputation'
url = 'https://app.powerbi.com/PleaseWait'

urlencode_url = urllib.quote_plus(url)

r = requests.get('{}/rest/app_run?_filter_action="{}"&_filter_message__icontains="{}"&page_size=0'
                 .format(auth['server'], action, urlencode_url), headers=headers, verify=False).json()

print(json.dumps(r, indent=4, sort_keys=True))

