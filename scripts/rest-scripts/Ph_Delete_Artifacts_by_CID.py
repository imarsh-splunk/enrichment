import requests


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

container_id = 306236
r = requests.get('https://{}/rest/artifact?_filter_container_id={}&page_size=0'
                 .format(host, container_id), headers=headers, verify=False).json().get('data')

name_exclude = 'vault artifact'

for i in r:
    aid = i.get('id')
    a_name = i.get('name')
    if a_name != name_exclude:
        d = requests.delete('https://{}/rest/artifact/{}'.format(host, aid), headers=headers, verify=False)
        r = d.content
        print(r)
