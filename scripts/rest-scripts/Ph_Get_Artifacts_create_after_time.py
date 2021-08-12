import requests

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

tag = ''
time = '2019-01-28'

r = requests.get('https://{}/rest/artifact?_filter_create_time__lt="{}"&page_size=0'
                 .format(host, time), headers=headers, verify=False)

# r = requests.get('https://{}/rest/artifact?_filter_tags__contains="{}"'
#                  '&page_size=0'.format(host, tag), headers=headers, verify=False)

r_data = r.json().get('data')

for item in r_data:
    # created = item['create_time']
    print(item)
