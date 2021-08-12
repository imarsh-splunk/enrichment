import requests
import json


def get_roi_summary(h, t):
    headers = {"ph-auth-token": auth['ph-auth-token']}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    try:
        r = requests.post('{}/query_portal_apps'.format(h), headers=headers, verify=False)
        return r.json()
    except Exception as e:
        # print(e)
        return e


auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}

get = get_roi_summary(auth['server'], auth['ph-auth-token'])
print(get)
