#! /usr/bin/env python2

from __future__ import print_function
import sys, json

def whole_file(filename):
    with open(filename) as f:
        return f.read()

def get_hashes(content):
    import hashlib
    return {
        "md5": hashlib.md5(content).hexdigest(),
        "sha1": hashlib.sha1(content).hexdigest(),
        "sha256": hashlib.sha256(content).hexdigest(),
    }

def get_attachments(raw_email):
    import email

    attachments = list()
    msg = email.message_from_string(raw_email)
    text = list()
    count = 0
    message_id = msg.get('message-id').strip()
    for part in msg.walk():
        if part.get('message-id'):
            message_id = msg.get('message-id').strip()
        content_type = part.get_content_type()
        filename = part.get_filename()
        content = part.get_payload(decode=1)
        charsets = part.get_charsets()

        new = {
            "message_id": message_id,
            "content_type": content_type,
        }
        if filename:
            new['filename'] = filename

        nonull_charsets = [x for x in charsets if x]
        if len(nonull_charsets):
            new['charsets'] = charsets

        if content:
            if len(nonull_charsets) > 0:
                new['text'] = content.decode(nonull_charsets[0])

            new.update({
                # taken out because python2 json.dumps can't figure out binary content
                #"content": content,
                "content": "<<binary>>",
                "hashes": get_hashes(content),
            })
        
        attachments += [new]

    return attachments

def phantom_rest(creds, endpoint, method="get", **kwargs):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    from requests.packages.urllib3.exceptions import InsecurePlatformWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

    headers = dict()
    auth = None
    if creds.get('token'):
        headers={"ph-auth-token": creds['token']}

    elif creds.get('username') and creds.get('password'):
        auth=(creds['username'], creds['password'])

    else:
        raise Exception("Error: credentials not found")

    if not creds.get('base_url'):
        raise Exception("Error: base url not found found")

    import re
    endpoint = re.sub("^rest/", "", endpoint.strip().strip("/"))
    url = re.sub("^(https*:/)", r"\1/", re.sub("/+", "/", "{}/rest/{}".format(creds['base_url'], endpoint)))

    print(url, file=sys.stderr)
    method = getattr(requests, method)

    if not method:
        raise Exception("Error: requests method not found; {}".format(method))

    if headers.keys():
        if not kwargs.get('headers'):
            kwargs['headers'] = dict()
        kwargs['headers'].update(headers)

    if auth:
        kwargs['auth'] = auth

    r = method(url, verify=False, **kwargs)
    if int(r.status_code) < 200 or int(r.status_code) >= 300:
        raise Exception("Error: rest call failed; {}", r.text)
    print("Status Code {}".format(r.status_code), file=sys.stderr)

    try:
        data = r.json()

    except:
        data = r.text

    return data, r

def save_artifact(creds, container, artifact, cef):
    new = {
        'name': "Artifact",
        'container_id': container,
        'type': "network",
        'label': "artifact",
        'cef': {},
    }

    if artifact:
        new.update(artifact)

    if cef:
        new['cef'].update(cef)

    data, r = phantom_rest(creds, endpoint="artifact", json=new, method="post")
    return data['id']

def add_attachment(creds, container, filename, content):
    if type(content) == bytes:
        import base64
        content = base64.b64encode(content).decode('utf8')

    new = {
        "container_id": container,
        "file_name": filename,
        "file_content": content,
    }

    data, r = phantom_rest(creds, endpoint="container_attachment", json=new, method="post")
    return data['succeeded']

creds = { 
    "token": "s3TrYpHX1OrWRi1CSeWIVxN9TJzi4jlKfabpGbibhP4=",
    "base_url": "https://192.168.1.173"
}

endpoint = "container/{}".format(sys.argv[1])
data, r = phantom_rest(creds, endpoint)
attachments = get_attachments(data['data']['raw_email'])
print(json.dumps(attachments, default=lambda x: str(type(x)), indent=4), file=sys.stderr)
