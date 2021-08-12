import requests

host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

label = "suspicious_email_submission"
status = "new"

r = requests.get('https://{}/rest/container?_filter_label="{}"&_status="{}"&page_size=0'
                 .format(host, label, status), headers=headers, verify=False)
# print(r.content)

containers = r.json().get('data')
# print(containers)

cids = []

for container in containers:
    # print(container)
    c_id = container.get('id')
    cids.append(c_id)

print(cids)
