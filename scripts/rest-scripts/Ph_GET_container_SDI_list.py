import requests

auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

# cname = "Failed login attempt"
cname = "Malicious URL Request Attempt"

r = requests.get('{}/rest/container/source_data_identifier'.format(auth['server']),
                 headers=headers, verify=False)
print(r.content)

