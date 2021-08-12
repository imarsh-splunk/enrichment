import requests
import json
import csv


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

list_id = 6
ep = '/rest/decided_list/{}'.format(list_id)
list_name = 'EDL-IP'

build_list = {
    "content": [
    ],
    "name": "{0}".format(list_name)
}

list_content = build_list['content']

flatfile = '/Users/cblumer/Documents/Ph_Testing_Data/HOT_FUEGO_TEST.csv'
with open(flatfile, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, fieldnames=['IP', 'Country', 'Timestamp'])

    # Define Column Headers
    # list_content.append(["IP", "Country", "Timestamp"])

    for row in csv_reader:
        print(row)
        col1 = row["IP"]
        col2 = row["Country"]
        col3 = row["Timestamp"]

        list_content.append([col1, col2, col3])

json_blob = json.dumps(build_list)

r = requests.post('https://{}{}'.format(host, ep), data=json_blob, headers=headers, verify=False)
print(r.json())
