# Create Phantom container via REST GET
import requests
import csv


def get_custom_list(h, t, list_id):

    ep = '/rest/decided_list/{}'.format(list_id)
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
custom_list_id = 1
custom_list = get_custom_list(host, token, custom_list_id)
print(custom_list)

csv_list = []

for item in custom_list['content']:

    item_str = item[0].encode('utf-8')

    #print(type(item_str))
    print(item_str)


    #csv_list.append(str(item[0])).encode('utf-8')

#with open("PAN_EDL.csv", 'w') as f:
#    w = csv.writer(f)
#    w.writerow(csv_list)



