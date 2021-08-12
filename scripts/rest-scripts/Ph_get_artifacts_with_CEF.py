import requests
import time

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
cef_key = 'sourceAddress'
param = '188.92.214.131'
now = int(time.time())
dayago = int(time.time()) - 86400

print(now)
print(dayago)

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

ep2 = '/rest/artifact?_filter_cef__{0}="{1}"&_filter_create_time="{2}"&page_size=0'.format(cef_key, param, dayago)
endpoint = '/rest/artifact?_filter_cef__{0}="{1}"&page_size=0'.format(cef_key, param)
r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()['data']

print(r)

for i in r:
    i_cef = i.get('cef')
    sA = i_cef.get('sourceAddress')
    cN = i_cef.get('countryName')
    tS = i.get('create_time')
    p = '%Y-%m-%dT%H:%M:%S.%fZ'
    epoch = int(time.mktime(time.strptime(tS, p)))
    print(sA, cN, tS, epoch)

# for item in r.json()['data']:
    # a_id = item.get('id')
    # c_id = item.get('container')

    # endpoint = '/rest/container/{0}'.format(c_id)
    # r = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False)
    # c_label = r.json().get('label')
    # print(r.content)

