import requests

host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

assets = requests.get('https://{}/rest/asset?page_size=0'.format(host), headers=headers, verify=False)

for asset in assets.json()['data']:
    name = asset['name']
    get_r = requests.get('https://{}/rest/asset?_filter_name="{}"'.format(host, name), headers=headers, verify=False)
    asset_config = get_r.json()['data'][0].get('configuration')

    if asset_config == {}:
        asset_vendor = get_r.json()['data'][0].get('product_vendor')

        # asset_id = get_r.json()['data'][0].get('id')
        # del_r = requests.delete('https://{}/rest/asset/{}'.format(host, asset_id), headers=headers, verify=False)

        print(asset_vendor)
