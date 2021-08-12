import requests


host = '10.0.0.124'
token = 'zQYRKnUNHLoXzBPxDTOWSwVcpWGuOwMYfZARBMlscnw='
# host = '172.16.101.177'
# token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

ep = "/rest/license_tracking?_filter_update_time__gt='2018-12-18T01:08:51.346000Z'"

psize = 0
r = requests.get('https://{}{}'.format(host, ep), headers=headers, verify=False).json().get('data')
# print(r)

for i in r:
    print(i)
