import requests
import json

host = '172.16.101.135'
token = 'Wy6uchQJIKC8cmXU4xNcWx0M5B/VE438fi+MxvdKU1I='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

new_fqdn = 'https://172.16.101.135'

post_dict = {
    "company_info_settings":
        {
            "administrator_contact": "cblumer@splunk.com",
            "fqdn": new_fqdn,
            "time_zone": "UTC",
            "company_name": "splunk"
        }
    }
data = json.dumps(post_dict)

endpoint = '/rest/system_settings'
r = requests.post('https://{}{}'.format(host, endpoint), headers=headers,  data=data, verify=False)
print(r.content)
