# Create Phantom container via REST GET
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


phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": token}

cl_name = 'REST API - Custom List Name'

#r = create_custom_list(host, token, cl_name)
#r_pretty = json.dumps(r.json(), indent=1)

#cl_id = json.loads(r.content)['id']

#print(r_pretty)

r = requests.get('https://xx.xx.xx.xx/rest/decided_list/{0}'.format(cl_id), headers=headers, verify=False)
r_pretty = json.dumps(r.json(), indent=1)
print(r_pretty)
