import requests
import json
from datetime import date, datetime, timedelta


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


def get_roi_dollars_saved_last_month(h, t):
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    now = datetime.utcnow()
    now = datetime.strptime(str(now), "%Y-%m-%d %H:%M:%S.%f")
    now_iso8601 = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    month_ago = datetime.strptime(str(datetime.utcnow() - timedelta(days=30)), "%Y-%m-%d %H:%M:%S.%f")
    month_ago_iso8601 = month_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    params = {"start_time": month_ago_iso8601,
              "end_time": now_iso8601}

    try:
        r = requests.get('https://{}/rest/widget_data/roi_stats?start_time={}&end_time={}'
                         .format(h, month_ago_iso8601, now_iso8601), headers=headers, verify=False)
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
# print(string_output)

roi_dollars_saved_last_month = get_roi_dollars_saved_last_month(host, token)
# print(roi_dollars_saved_last_month)

# for i in roi_dollars_saved_last_month:
    # print(i)

month_dollar_total = sum(item['y'] for item in roi_dollars_saved_last_month)
# print(month_dollar_total)

output = ("USD Amount Saved in last 30 days: ${number:.{digits}f}".format(number=month_dollar_total, digits=2))
print(output)
