import requests
import json

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

r = requests.get('https://{}/rest/audit?format=json&user&role&authentication&playbook&container&tenant'
                 .format(host), headers=headers, verify=False)

r_json_pretty = json.dumps(r.json(), indent=1)
print(r_json_pretty)

# audit_timestamps = []
# audit_notes = []

# for entry in r.json():
#    note = entry['NOTE']
#    audit_notes.append(note)

    # user = entry['USER']

#    time = entry['TIME']
#    audit_timestamps.append(time)

    # activity = entry['AUDIT SOURCE']

# print(audit_timestamps)
# for item in audit_timestamps:
    # print(item)

# print(audit_notes)
# for item in audit_notes:
    # print(item)

# audit_modified_values = []

# for entry in r.json():
    # if entry['NEW VALUE'] != entry['OLD VALUE']:

        # print("Old value:{} AND New value:{}".format(entry['OLD VALUE'], entry['NEW VALUE']))
        # audit_modified_values.append("Old value:{} AND New value:{}".format(entry['OLD VALUE'], entry['NEW VALUE']))

# print(audit_modified_values)
