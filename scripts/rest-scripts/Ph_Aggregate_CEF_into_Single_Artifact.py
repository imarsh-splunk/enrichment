import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

container_id = 33
r = requests.get('https://{}/rest/artifact?_filter_container_id={}&page_size=0'
                 .format(host, container_id), headers=headers, verify=False).json()['data']

all_cef = []

for i in r:
    all_cef.append(i.get('cef'))

print(all_cef['atpEventData'])

# event_data = ', '.join(d['eventUUID'] for d in all_cef)

# print(event_data)

endpoint = '/rest/artifact'
a_name = 'Aggregated Event Artifact'

artifact_json = {
        "cef": {
            "atpEventData": "{}".format(event_data)
        },
        "name": a_name,
        "container_id": container_id,
        "label": "event",
        "run_automation": False,
        "severity": "low",
        "type": "ticketing"
    }
json_blob = json.dumps(artifact_json)

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()
r = requests.post('https://{}{}'.format(host, endpoint), data=json_blob, headers=headers, verify=False)
print(r.content)