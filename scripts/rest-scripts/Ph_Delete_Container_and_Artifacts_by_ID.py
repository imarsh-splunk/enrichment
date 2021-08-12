import requests

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 3354

r = requests.get('https://{}/rest/artifact?_filter_container_id={}&page_size=0'
                 .format(host, cid), headers=headers, verify=False).json()['data']

for a in r:
    aid = a.get('id')
    d = requests.delete('https://{}/rest/artifact/{}'.format(host, aid), headers=headers, verify=False)
    r = d.content
    print('Artifact DELETE Response: {}'.format(r))


d = requests.delete('https://{}/rest/container/{}'.format(host, cid), headers=headers, verify=False)
r = d.content
print('Container DELETE Response: {}'.format(r))
