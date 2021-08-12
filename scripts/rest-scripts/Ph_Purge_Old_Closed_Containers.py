import requests
from datetime import date
from dateutil.relativedelta import relativedelta


host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

six_months = date.today() - relativedelta(months=1)

r = requests.get('https://{}/rest/container?_filter_status="closed"&_filter_create_time__lt="{}"&page_size=0'.format(host, six_months),
                 headers=headers, verify=False)
containers = r.json().get('data')

ids = []

for i in containers:
    c_id = i.get('id')
    ids.append(c_id)
# print(ids)

id_csv = ','.join(map(str, ids))
print(id_csv)
