import requests


def get_custom_list(h, t, i):

    ep = '/rest/decided_list/{}'.format(i)
    # formatted_content?_output_format=csv
    headers = {"ph-auth-token": t}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()
    r = requests.get('https://{}{}'.format(h, ep), headers=headers, verify=False)
    return r.json()


host = '10.0.0.3'
token = 'BNVu14chEJVMLBfZzWCG+CAbheGzSvDgKzwlkWYLkUo='
list_id = 6

cl = get_custom_list(host, token, list_id)['content']
#print(cl)

gen = []

for row in cl:
    ip = row[0]
    cn = row[1]
    append = {'phantom_eventName': 'Signal Sciences WAF Alert',
              'sourceAddress': ip,
              'countryName': cn}
    gen.append(append)

with open('/users/cblumer/Desktop/gen.txt', 'w') as f:
    for item in gen:
        f.write("{}\n".format(item))

print(gen)


