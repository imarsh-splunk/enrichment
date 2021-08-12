import requests
import json


def create_custom_list(h, t, cl_name):

    ep = '/rest/decided_list'

    cl_json = {
        "content": [
            [
                "10.0.0.0/8"
            ],
            [
                "172.16.0.0/12"
            ],
            [
                "192.168.0.0/16"
            ]
        ],
        "name": "{}".format(cl_name)
    }

    json_blob = json.dumps(cl_json)

    head = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    req = requests.post('https://{}{}'.format(h, ep), data=json_blob, headers=head, verify=False)
    return req


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}

cl_name = 'REST API - Custom List Name'

r = create_custom_list(host, token, cl_name)
r_pretty = json.dumps(r.json(), indent=1)

print(r_pretty)
