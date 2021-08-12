import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

name = 'ewso365'
asset_id = requests.get('https://{}/rest/asset?_filter_name="{}"'
                        .format(host, name), headers=headers, verify=False).json()['data'][0]['id']

py_file = str(open("preprocess.py", "r").read())
# print(py_file)

update_data = {
   "configuration": {
       "preprocess_script": py_file
   }
}

update_json = json.dumps(update_data)

post = requests.post('https://{}/rest/asset/{}'.format(host, asset_id), headers=headers, data=update_json, verify=False)
print(post.content)
