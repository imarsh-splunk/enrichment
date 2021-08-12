import requests
import json

host = '172.16.101.135'
token = 'Wy6uchQJIKC8cmXU4xNcWx0M5B/VE438fi+MxvdKU1I='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

post_dict = {'debug_settings':
                 {'actiond_debug_level': 1,
                  'workflowd_debug_level': 1,
                  'watchdogd_debug_level': 1,
                  'clusterd_debug_level': 1,
                  'decided_debug_level': 1,
                  'ingestd_debug_level': 1
                  }
             }

data = json.dumps(post_dict)

endpoint = '/rest/system_settings'
r = requests.post('https://{}{}'.format(host, endpoint), headers=headers,  data=data, verify=False)
print(r.content)
