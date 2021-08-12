import requests

host = '172.16.101.158'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 1308
ep = '/rest/container/{}/export?file_list[]=60'.format(cid)
r = requests.get('https://{}{}'.format(host, ep), headers=headers, verify=False)
f = open('container.tgz', 'wb').write(r.content)
