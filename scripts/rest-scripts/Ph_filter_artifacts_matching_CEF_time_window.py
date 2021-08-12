import requests
from datetime import datetime, timedelta

host = '172.16.101.177'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cef_key = 'parsedSubject'
time = datetime.utcnow() - timedelta(hours=48)

endpoint = '/rest/artifact/?_filter_cef__{}__isnull=False&_filter_create_time__gt="{}"&page_size=0'\
    .format(cef_key, time)
r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False)

print(r.content)
