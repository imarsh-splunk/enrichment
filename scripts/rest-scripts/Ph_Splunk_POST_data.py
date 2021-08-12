import requests
import json

url = 'https://172.16.x.y:8088/services/collector/event'
authHeader = {'Authorization': 'Splunk super_sekrit'}

jsonDict = {"event": "through python -- again - does this thing work"}

r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)
print (r.text)
