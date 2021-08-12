import requests
import json

host = '172.16.101.168'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

endpoint = '/rest/ph_user?_filter_type__in=["normal"]&page_size=0'

r = requests.get('https://{}{}'.format(host, endpoint),
                 headers=headers, verify=False).json()['data']

for user in r:
    print(user)
    field = user.get('show_onboarding')

    if field is True:

        uid = user.get('id')
        endpoint = '/rest/ph_user/{}'.format(uid)
        data = {"show_onboarding": False}
        # r = requests.post('https://{}{}'.format(host, endpoint), headers=headers, data=json.dumps(data), verify=False)
        # print(r.content)
