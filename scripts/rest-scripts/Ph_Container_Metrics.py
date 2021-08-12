import requests
import json


def countContainers(label, severity, status, tag, timeframe):
    try:
        host = '10.0.0.16'
        url = 'https://%s/rest/container?page=0&page_size=1' % (host)

        if label:
            url = url + '&_filter_label__contains="%s"' % (label)
        if severity:
            url = url + '&_filter_severity="%s"' % (severity)

        if status:
            url = url + '&_filter_status="%s"' % (status)

        if tag:
            url = url + '&_filter_tags=["%s"]' % (tag)

        if timeframe:
            url = url + '&_filter_create_time__gt="%s"' % (timeframe)

        t = 'tOPrt24rDK5FxZluW//QtsKuIV2gPL4kDRa1/BHLCV8='
        head = {"ph-auth-token": t}

        # disable certificate warnings for self signed certificates
        requests.packages.urllib3.disable_warnings()

        r = requests.get(url, headers=head, verify=False)

        # Verifying if query was successful
        if r is None or (r.status_code != 200 and r.status_code != 400):
            if r is None:
                print('Error running query')
            else:
                print('Error: %s - %s', r.status_code, json.loads(r.text)['message'])
            return '0'

        # Query was successful
        content = json.loads(r.text)
        count = content.get('count', "0")
        return count
    except Exception as e:
        print('Error: %s', e.args[0])


label = 'events'
sev = 'medium'
status = 'new'
tags = 'snow'


timeframe = ''

print (countContainers(label, sev, status, tag, timeframe))

