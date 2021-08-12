import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import os

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

# SET stored timestamp
threshold = date.today() - relativedelta(minutes=15)
# print(threshold)
os.environ['phantom_container_update_timestamp'] = str(threshold)
# print(os.environ['phantom_container_update_timestamp'])

# GET stored timestamp
# threshold = os.environ['phantom_container_update_timestamp']
# print(threshold)

r = requests.get('https://{}/rest/container?_filter_container_update_time__gt="{}"&page_size=0'
                 .format(host, os.environ['phantom_container_update_timestamp']), headers=headers, verify=False)
containers = r.json().get('data')
# print(containers)

cids = []

for container in containers:
    # print(container)
    # c_id = container.get('id')
    cids.append(container)

print(cids)
