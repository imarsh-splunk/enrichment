import requests


def get_audit_logs(h, t, s):
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    try:
        r = requests.get('{0}/rest/audit?sort=TIME&start={1}'.format(h, s), headers=headers, verify=False)
        return r.json()
    except Exception as e:
        print(e)


auth = {
  "ph-auth-token": "tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8=",
  "server": "https://10.0.0.16"
}
start_date = '2020-01-01'

audit_json = get_audit_logs(auth['server'], auth['ph-auth-token'], start_date)

for i in audit_json:
    print(i)

