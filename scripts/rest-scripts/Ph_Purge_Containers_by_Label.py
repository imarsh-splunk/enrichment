import requests

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()


label = 'signalsciences-purge'
limit = 0  # set to 0 to return all containers (may take a very long time to return if a lot of data)
endpoint = '/rest/container?_filter_label="{0}"&page_size={1}'.format(label, limit)

r = requests.get('https://{}{}'.format(host, endpoint),
                 headers=headers, verify=False).json()

c_count = r.pop('num_pages')  # page_size must be set to 1 to get the container count
c_data = r.pop('data')

id_list = []

for c in c_data:
    id_list.append(c.pop('id'))

for i in id_list:
    d = requests.delete('https://{}/rest/container/{}'.format(host, i), headers=headers, verify=False)
    r = d.content
    print('Container ID: {} - Delete Container Response: {}'.format(i, r))
