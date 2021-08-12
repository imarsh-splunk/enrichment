import requests

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

r = requests.get('https://{}:443'.format(host), verify=False)
print(r.content)

