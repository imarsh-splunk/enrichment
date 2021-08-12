import requests

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

c_id = '3437'
c_artifacts = requests.get('https://{}/rest/artifact?_filter_container_id__={}&page_size=0'.format(host, c_id),
                           headers=headers, verify=False).json()['data']

a_names = ['Domain Artifact', 'URL Artifact', 'Vault Artifact']

for a in c_artifacts:
    if a['name'] not in a_names:

        print(a)
