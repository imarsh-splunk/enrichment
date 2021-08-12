import requests
from datetime import *
import csv
import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
host = 'sftp.emc.com'
port = 22
user = 'CityNationalBank'
pw = 'GEe9aMLDd'

try:
    ssh.connect(host, port, username=user, password=pw)
except paramiko.SSHException:
    print("Connection Error")

local_path = "/var/tmp/IP_RBC_(CNB).csv"
sftp = ssh.open_sftp()
sftp.chdir('/')

# Download the latest "IP_RBC_(CNB)_*.csv" to /var/tmp on the Phantom host
for remote_file in sftp.listdir_attr():
    if remote_file.filename.startswith('IP_RBC_(CNB)_'):
        remote_path = '/' + remote_file.filename
        m_time_epoch = sftp.stat(remote_path).st_mtime
        last_modified = datetime.fromtimestamp(m_time_epoch)

        if (datetime.now() - last_modified) <= timedelta(hours=24):
            sftp.get(remote_path, local_path)
        else:
            # Delete all "IP_RBC_(CNB)_*.csv" which were not created in the last 24 hours
            sftp.remove(remote_path)
sftp.close()
ssh.close()

# Connect to Phantom REST API and add new artifacts to container for each row in the CSV
host = '172.16.101.133'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
requests.packages.urllib3.disable_warnings()

try:
    f = open(local_path, "r")
    reader = csv.DictReader(f)

    for row in reader:
        c_id = 1022
        artifact_name = 'IP - Row Artifact'
        artfact_label = 'IP_RBC'
        artifact_type = 'threat_intel'

        artifact_json = {
            "cef": {
                "ipAddress": "{}".format(row["IP"]),
                "portNumber": "{}".format(row["Port"]),
                "typeName": "{}".format(row["Type"]),
                "comment": "{}".format(row["Comment"])
        },
            "container_id": "{}".format(c_id),
            "name": "{}".format(artifact_name),
            "label": "{}".format(artfact_label),
            "run_automation": False,
            "type": "{}".format(artfact_label)
        }

        artifact_r = requests.post('https://{}/rest/artifact'.format(host), data=json.dumps(artifact_json),
                                   headers=headers, verify=False)
        print(artifact_r.content)


except TypeError as e:
    print("There was not a new IP_RBC(CNB)_*.csv file available on the SFTP server. Error: {}".format(e))


