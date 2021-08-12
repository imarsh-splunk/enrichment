import requests

host = 'xxx.16.101.158'
token = 'xxx39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='

headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

cid = 1308
ep = '/rest/container/{}/export'.format(cid)
r = requests.get('https://{}{}'.format(host, ep), headers=headers, verify=False)
f = open('container.tgz', 'wb').write(r.content)
