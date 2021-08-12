import requests
import csv

auth = {
  "ph-auth-token": "qckSOihgm1kGwreeZ+9wBSH7rAGQau/7y0xNUG6fewU=",
  "server": "https://10.0.0.16"
}
headers = {"ph-auth-token": auth['ph-auth-token']}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/ph_user?page_size=0'

user_list = requests.get('{}{}'.format(auth['server'], endpoint), headers=headers, verify=False).json()['data']

with open('phantom_user_export.csv', 'w') as output_file:
    w = csv.DictWriter(output_file, fieldnames=user_list[0].keys())
    w.writeheader()

    for user in user_list:
        w.writerow(user)
