import requests
import json

host = '10.0.0.125'
token = 'Dn8HVagP2J/BbC3l4RD3h0MKcoJLjH26wMB0kwI7R/U='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

a_id = 3398
endpoint = '/rest/artifact/{}'.format(a_id)
tag_list = requests.get('https://{}{}'.format(host, endpoint), headers=headers, verify=False).json()['tags']

new_tag = 'new_tag1'
u_new_tag = unicode(new_tag, 'utf_8')
tag_list.append(u_new_tag)

post_data = {
    "tags": tag_list
}

json_blob = json.dumps(post_data)
r = requests.post('https://{}{}'.format(host, endpoint), data=json_blob, headers=headers, verify=False)

print(r.content)
