import csv
import requests
import argparse
import json


def csv_parser(csv_file):
    return(list(csv.reader(csv_file)))


def upload_file(arguments):
    csv_list = csv_parser(arguments.file)
    url = arguments.url
    
    if url[-1] == '/':
        url = url[0:-1] 

    url = url + '/rest/decided_list'

    if arguments.append:
        url = url + '/' + arguments.list
        data = {"append_rows": csv_list}
    else:
        data = {"content": csv_list, "name": arguments.list}

    response = _send_request(url, 'post', arguments.token, not(arguments.do_not_verify), payload=json.dumps(data))

    message = 'Successfully ' + ('appended' if arguments.append else 'added') + ' list'

    if ('success' in response and not(response['success'])) or 'success' not in response:
        message = 'Unable to update/add list: ' + str(response)
    
    return(message)


def _send_request(url, method, token, verify_cert, payload=None, content_type=None):
    
    url = url
    request_func = getattr(requests, method.lower())
    
    if request_func is None:
        raise ValueError('Incorrect requests action specified')

    try:
        r = request_func(
            url,
            headers={'ph-auth-token': token},
            data=payload,
            verify=verify_cert,
            auth=None
        )

        r.raise_for_status
    except requests.exceptions.SSLError as err:
        raise Exception(
            'Error connecting to API - '
            'Likely due to the "validate server certificate" option. '
            'Details: ' + str(err)
        )
    except requests.exceptions.HTTPError as err:
        raise Exception(
            'Error calling - ' + url + ' - \n'
            'HTTP Status: ' + r.status
            + 'Reason: ' + r.reason
            + 'Details: ' + str(err)
        )
    except requests.exceptions.RequestException as err:
        raise Exception(
            'Error calling - ' + url + ' - Details: ' + str(err)
        )

    try:
        results = r.json()
    except ValueError:
        results = r.text

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload csv file to custom list')
    parser.add_argument('-u', '--url', help='Phantom Base URL ex: https://phantom.localhost', required=True)
    parser.add_argument('-t', '--token', help='Phantom api token', required=True)
    parser.add_argument('-f', '--file', help='CSV File to upload', type=argparse.FileType('r'), required=True)
    parser.add_argument('-l', '--list', help='Name of phantom custom list', required=True)
    parser.add_argument('-d', '--do_not_verify', help='(Optional) Do no verify server cert', action="store_true", default=False)
    parser.add_argument('-a', '--append', help='(Optional) Append to existling list', action="store_true", default=False)

    arguments = parser.parse_args()
    
    print arguments.url
    
    print(upload_file(arguments))