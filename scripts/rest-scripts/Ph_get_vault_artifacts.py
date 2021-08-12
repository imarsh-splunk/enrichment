import requests

host = '172.16.101.177'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

r = requests.get('https://{}/rest/artifact?page_size=0'.format(host),
                 headers=headers, verify=False).json()['data']
# print(r)

for i in r:
    name = i["name"]
    if name == "Vault Artifact":
        cef = i["cef"]
        name = cef.get("name")
        contentType = cef.get("contentType")
        print(name, contentType)
