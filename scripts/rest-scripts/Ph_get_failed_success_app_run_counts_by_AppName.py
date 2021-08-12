import requests

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

app_name = "VirusTotal"
r = requests.get('https://{}/rest/app_run?_filter_app_name="{}"&page_size=0'
                 .format(host, app_name), headers=headers, verify=False).json()['data']

success_list = []
failed_list = []

for i in r:
    if i['status'] == 'success':
        success_list.append(i)
    elif i['status'] == 'failed':
        failed_list.append(i)

success_count = len(success_list)
failed_count = len(failed_list)

print("Count of Successful VirusTotal App Actions: {}".format(success_count))
print("Count of Failed VirusTotal App Actions: {}".format(failed_count))
