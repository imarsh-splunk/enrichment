import requests


def return_filtered_containers(ph_host, api, param):

    headers = {"ph-auth-token": api}
    # disable certificate warnings for self signed certificates
    requests.packages.urllib3.disable_warnings()

    statuses = ['new', 'open', 'closed']
    severities = ['low', 'medium', 'high']

    try:
        if param in statuses:
            endpoint = '/rest/container?_filter_status="{0}"'.format(param)
            r = requests.get('https://{}{}'.format(ph_host, endpoint), headers=headers, verify=False)
            return r.json()['data']

        elif param in severities:
            endpoint = '/rest/container?_filter_severity="{0}"'.format(param)
            r = requests.get('https://{}{}'.format(ph_host, endpoint), headers=headers, verify=False)
            return r.json()['data']

    except TypeError as e:
        error = ('The param input was not excepted - Error: {}'.format(e))
        return error


phantom_host = 'xx.xx.xx.xx'
AUTH_TOKEN = 'xxxx'
status = 'open'

try:
    containers = return_filtered_containers(host, token, param)
    populated_containers = []
    empty_containers = []

    for container in containers:
        c_id = container.get('id')
        c_name = container.get('name')
        a_count = container.get('artifact_count')

        if a_count != 0:
            populated_containers.append([c_id, c_name])
            # print ('Container ID {0} has {1} Artifacts'.format(c_id, a_count))
        else:
            empty_containers.append([c_id, c_name])
            # print ('Container ID {0} has {1} Artifacts'.format(c_id, a_count))

    for c in populated_containers:
        print (c)

except TypeError as e:
    print('The param input was not excepted - Error: {0}'.format(e))

