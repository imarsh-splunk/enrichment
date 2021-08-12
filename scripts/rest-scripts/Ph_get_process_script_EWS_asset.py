import requests
import json

host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

name = 'ewso365'
r = requests.get('https://{}/rest/asset?_filter_name="{}"'.format(host, name), headers=headers, verify=False)
# print(r.content)
rjson = json.dumps(r.json(), indent=1)
print(rjson)

preprocess_script = str(r.json()['data'][0]['configuration']['preprocess_script'])
# print(preprocess_script)

with open("preprocess.py", "w") as py_file:
    py_file.write(preprocess_script)

# py_file = open("preprocess.py", "r")
# print(py_file.read())


