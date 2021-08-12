import requests


def get_all_custom_list(h, t):

    ep = '/rest/decided_list?page_size=0'
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


def get_custom_list_contents(h, t, i):

    ep = '/rest/decided_list/{}'.format(i)
    # formatted_content?_output_format=csv
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='

all_lists = get_all_custom_list(host, token)

for item in all_lists['data']:
    list_name = item['name']
    list_id = item['id']
    list_contents = get_custom_list_contents(host, token, list_id)
    content_length = len(list_contents['content'])
    print(list_name, content_length)
