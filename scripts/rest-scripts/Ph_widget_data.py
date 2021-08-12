import requests
import json


def get_roi_summary(h, t):
    headers = {"ph-auth-token": auth['ph-auth-token']}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    try:
        r = requests.get('{}/rest/widget_data'
                         .format(h), headers=headers, verify=False)
        return r.json()
    except Exception as e:
        print(e)


auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}

roi_output = get_roi_summary(auth['server'], auth['ph-auth-token'])

perf = roi_output['containers_performance']

for i in perf:
    print(i)
