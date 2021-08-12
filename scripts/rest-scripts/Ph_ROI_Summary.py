import requests
import json


def get_roi_dollars_saved(h, t):
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    try:
        r = requests.get('https://{}/rest/widget_data/roi_stats'
                         .format(h), headers=headers, verify=False)
        return r.json()['dollars_saved']
    except Exception as e:
        print(e)


host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='

roi_dollars_saved_output = get_roi_dollars_saved(host, token)
# print(roi_dollars_saved_output)

metrics_output = []

for i in roi_dollars_saved_output:
    i['USD_Dollar_Value'] = i.pop('y')
    i['Calendar_Day'] = i.pop('x')
    i['Calendar_Day'] = i['Calendar_Day'].replace('T00:00:00Z', '')
    metrics_output.append(json.dumps(i).replace('{', '').replace('}', ''))

string_output = '\n'.join(metrics_output)
print(string_output)




