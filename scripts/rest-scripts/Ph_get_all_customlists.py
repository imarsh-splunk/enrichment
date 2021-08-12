import requests


def get_custom_list(h, t):

    ep = '/rest/decided_list?page=0'
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='

all_lists = get_custom_list(host, token)

print(all_lists)

sorting_key = 'id'
sorted_lists = sorted(all_lists['data'], key=lambda k: k[sorting_key])

# for item in sorted_lists:
#    print(item)
