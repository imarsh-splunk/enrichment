import requests


def get_vault_item_info(c):
    r = requests.get('https://{}/rest/container_attachment?_filter_container={}'
                     .format(host, c), headers=headers, verify=False)
    vault_items = r.json().get('data')

    item_ids = []

    for item in vault_items:
        item_id = item.get('vault_document')
        item_ids.append(item_id)

    item_info = []

    for i_id in item_ids:
        r = requests.get('https://{}/rest/vault_document?_filter_id={}'
                         .format(host, i_id), headers=headers, verify=False)
        item_info.append(r.json())

    return item_info


host = '172.16.101.133'
token = 'CbQ39z73k83KEMh4ggwZT+nS/hQgT/fcIm28nrX5qIU='
headers = {"ph-auth-token": token}
requests.packages.urllib3.disable_warnings()

c_id = 1022
items = get_vault_item_info(c_id)

item_sha1s = []

for i in items:
    sha1 = i['data'][0].get('hash')
    item_sha1s.append(sha1)

print(item_sha1s)

