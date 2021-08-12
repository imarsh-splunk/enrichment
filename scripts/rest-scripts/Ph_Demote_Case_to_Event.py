import requests
import json

auth = {
    "ph-auth-token": "Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U=",
    "server": "https://10.0.0.125"
}

# auth = {
#  "ph-auth-token": "tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8=",
#  "server": "https://10.0.0.16"
# }

headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 280617
ep = "/rest/container/{}".format(cid)

# r = requests.get("{}{}".format(auth['server'], ep), headers=headers, verify=False)

payload = {"container_type": "default"}
r = requests.post("{}{}".format(auth['server'], ep), data=json.dumps(payload), headers=headers, verify=False)

print(r.content)
