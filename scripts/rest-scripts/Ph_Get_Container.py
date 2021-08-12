# Return Phantom Container by ID
import requests
import json
import re

phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
headers = {"ph-auth-token": AUTH_TOKEN}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/container/'
container_id = '15'

r = requests.get('https://{}{}{}'.format(phantom_host, endpoint, container_id),
                 headers=headers, verify=False)
r_dict = r.json()
r_json_pretty = json.dumps(r_dict, indent=1)
# Individual values from JSON object response
parent_container = r_dict['parent_container']
in_case = r_dict['in_case']
closing_rule_run = r_dict['closing_rule_run']
sensitivity = r_dict['sensitivity']
closing_owner = r_dict['closing_owner']
create_time = r_dict['create_time']
source_data_identifier = r_dict['source_data_identifier']

# Accessing CEF data fields
#raw_email = r_dict['data']['raw_email']

# Parsing strings within a CEF data field
#raw_email_subject = re.findall(r'Subject: (.*?)Thread-Topic:', raw_email, re.DOTALL)
#subject1 = raw_email_subject[0]
#subject2 = raw_email_subject[1]

print r_json_pretty
