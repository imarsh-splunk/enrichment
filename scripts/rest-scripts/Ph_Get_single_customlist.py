import requests


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='

ep = '/rest/decided_list/16/formatted_content?_output_format=csv'
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()
r = requests.get('https://{}{}'.format(host, ep), headers=headers, verify=False)

print(r.content)


