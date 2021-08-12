import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import os
from subprocess import Popen, PIPE
import subprocess
import logging

# logging
LOG = "/tmp/delete_containers.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)

# console handler
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)

# time tracking
utc_now = datetime.strptime(str(datetime.utcnow()), "%Y-%m-%d %H:%M:%S.%f")
logging.debug("Script started at UTC: {}".format(utc_now))

# build headers for GET request
auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

ep = '/rest/container_status'
r = requests.get('{}{}'.format(auth['server'], ep), headers=headers, verify=False).json().get('data')

open_new = []
resolved = []
for i in r:
    if i['status_type'] in ['open', 'new']:
        open_new.append(i['id'])
    elif i['status_type'] == 'resolved':
        resolved.append(i['id'])

# generate timestamp for fetching containers
month = date.today() - relativedelta(months=1)
months = date.today() - relativedelta(months=3)
year = date.today() - relativedelta(months=12)

# GET request 1 - EVENTS in 'open' or 'new' status older than 30 days
r1 = requests.get('{}/rest/container?_filter_container_type="default"&_filter_status__in={}&_filter_create_time__lt="{}"&page_size=0'.format(auth['server'], open_new, month), headers=headers, verify=False)
logging.debug("GET request status_code returned: {}".format(r1.status_code))
containers1 = r1.json().get('data')
logging.debug("Number of containers retrieved (open or new events older than 30 days): {}".format(len(containers1)))

# GET request 2 - EVENTS in 'resolved' status older than 90 days
r2 = requests.get('{}/rest/container?_filter_container_type="default"&_filter_status__in={}&_filter_create_time__lt="{}"&page_size=0'.format(auth['server'], resolved, months), headers=headers, verify=False)
logging.debug("GET request status_code returned: {}".format(r2.status_code))
containers2 = r2.json().get('data')
logging.debug("Number of containers retrieved (resolved events older than 90 days): {}".format(len(containers2)))

# GET request 3 - CASES in any status older than 1 year
r3 = requests.get('{}/rest/container?_filter_container_type="case"&_filter_create_time__lt="{}"&page_size=0'.format(auth['server'], year), headers=headers, verify=False)
logging.debug("GET request status_code returned: {}".format(r3.status_code))
containers3 = r3.json().get('data')
logging.debug("Number of containers retrieved (cases older than 1 year): {}".format(len(containers3)))

# combine retrieved list into a single list
containers = containers1 + containers2 + containers3
# print(containers)

ids = []

for i in containers:
    if "\\r\\n" not in i['name']:
        c_id = i.get('id')
        ids.append(c_id)

logging.debug("Total number of containers to delete: {}".format(len(ids)))
logging.debug("Script ended at UTC: {}".format(utc_now))

if ids:
    batch = 1000

    for count, i in enumerate(range(0, len(ids), batch)):
        cids = ','.join(map(str, ids[i:i + batch]))
        logging.debug("Batch {} - Container IDs: {} \n".format(count, cids))
        try:
            # logging.debug("Executing delete_containers.pyc script. Current UTC time: {}".format(utc_now))
            del_script = Popen(['sudo', 'phenv', 'python', '/opt/phantom/bin/delete_containers.pyc', '-i', '{}'.format(cids)], stdout=PIPE, stderr=PIPE)
            del_script.communicate(input=b'y')
            logging.debug("Containers successfully purged with delete_containers.pyc script. UTC time: {}".format(utc_now))

        except Exception as e:
            logging.debug("ERROR: {}".format(e))

else:
    logging.debug("No Container IDs found matching given criteria.. Exiting Script.")