import os
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from subprocess import Popen,PIPE

# backup phantom to nfs share
os.system("sudo phenv python2.7 /opt/phantom/bin/backup.pyc --all --backup-path /freenas_nfs/")

# query for containers to purge (created more than 30 days ago and closed status)
host = '127.0.0.1'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

1monthago = date.today() - relativedelta(months=1)

r = requests.get('https://{}/rest/container?_filter_status="closed"&_filter_create_time__lt="{}"&page_size=0'.format(host, 1monthago),
                 headers=headers, verify=False)
containers = r.json().get('data')

ids = []

for i in containers:
    c_id = i.get('id')
    ids.append(c_id)

id_csv = ','.join(map(str, ids))

# delete containers
del_script = Popen(['sudo', 'phenv', 'python2.7', '/opt/phantom/bin/delete_containers.pyc', '-i', '{}'.format(id_csv)], stdin=PIPE, stdout=PIPE)
del_script.communicate(input='y')
