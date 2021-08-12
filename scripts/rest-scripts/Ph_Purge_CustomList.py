import requests
import time
import json


def get_custom_list(h, t, i):

    ep = '/rest/decided_list/{}'.format(i)
    # formatted_content?_output_format=csv
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


def create_custom_list(i, h, t, n, c):

    ep = '/rest/decided_list/{}'.format(i)

    cl_json = {
        "content": c,
        "name": "{}".format(n)
    }

    json_blob = json.dumps(cl_json)

    head = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    req = requests.post('https://{}{}'.format(h, ep), data=json_blob, headers=head, verify=False)
    return req.content


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
list_id = 6

cl = get_custom_list(host, token, list_id)["content"]

# Items added within 24 hrs. ago
exp = int(time.time()) - 86400
new_list = []

for i in cl:
    if int(i[2]) > exp:
        new_list.append(i)

cl_name = 'HOT_FUEGO'
r = create_custom_list(list_id, host, token, cl_name, new_list)

print(r)
