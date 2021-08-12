# Create Phantom container via REST GET
import requests
import json
import csv


phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

list_id = 7
ep = '/rest/decided_list/{}'.format(list_id)
list_name = 'CG_Threatlist_Domain'
list_json = {
    "content": [
        [
            ""
        ]
    ],
    "name": "{0}".format(list_name)
}

print(type(list_json))
print(list_json)

flatfile = '/Users/cblumer/Documents/Ph_Testing_Data/CG_Threatlist_Domain.csv'
#with open(flatfile, mode='r') as csv_file:
    #csv_reader = csv.DictReader(csv_file)
    #for row in csv_reader:
        # print(row['domain'])


#print(list_content)

#r = requests.post('https://{}{}'.format(host, ep), data=json_blob, headers=headers, verify=False)
#print(r.json())


