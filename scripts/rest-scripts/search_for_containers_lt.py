import requests
from datetime import date
from dateutil.relativedelta import relativedelta


host = 'xx.0.0.124'
token = 'xxxxKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

one_month = date.today() - relativedelta(months=1)

r = requests.get('https://{}/rest/container?_filter_create_time__lt="{}"&page_size=0'.format(host, one_month),
                 headers=headers, verify=False)
containers = r.json().get('data')
print(containers)

ids = []

for i in containers:
    c_id = i.get('id')
    ids.append(c_id)
# print(ids)

id_csv = ','.join(map(str, ids))
print(id_csv)
