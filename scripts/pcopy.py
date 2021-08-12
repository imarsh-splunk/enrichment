#!/usr/bin/env python3

VERSION = 1.2
VERIFY_CERT = False
OUTPUT_DIR = "ph_config"
ITEMS = {
    "system_settings": {
        "mobile": True,
        "clickable_urls": True,
        "multi_tenant": True,
        "whitelist": True,
        "indicators": True,
        "audit_trail_settings": True,
        "auth_settings": True
    },
    "role": True,
    "cef": True,
    "container_status": True,
    "severity": True,
    "labels": True,
    "custom_fields": True,
    "tags": True,
    "container_pin_settings": True 
}

def clean_json(item, data):

    if item == "system_settings":
        new_data = {}
        for key, value in data.items():
            if key not in ["audit_trail_settings", "auth_settings"]:
                new_data['feature'] = key
                new_data['set_feature_enabled'] = value['enabled']
            else:
                new_data = data

    elif item == "custom_fields":
        new_data = {}
        new_data['update_container_custom_fields'] = True
        new_data['fields'] = json.dumps(data)

    elif item == "role":
        new_data = []
        for item in data['data']:
            new_item = item
            if new_item['immutable'] is True:
                continue
            del new_item['id']
            new_data.append(new_item)

    elif item == "cef":
        new_data = []
        for item in data['data']:
            new_item = item
            if new_item['type'] == "default":
                continue
            del new_item['id']
            new_data.append(new_item)

    elif item == "container_status":
        new_data = []
        for item in data['data']:
            new_item = item
            if new_item['is_default'] is True or new_item['is_mutable'] is False:
                continue
            del new_item['id']
            del new_item['disabled']
            new_data.append(new_item)

    elif item == "severity":
        new_data = []
        for item in data['data']:
            new_item = item
            if new_item['name'] in ["high", "medium", "low"]:
                continue
            del new_item['id']
            del new_item['disabled']
            new_data.append(new_item)

    elif item == "labels":
        new_data = []
        for item in data['label']:
            new_item = {}
            new_item['add_label'] = True
            new_item['label_name'] = item
            new_data.append(new_item)

    elif item == "tags":
        new_data = []
        for item in data['tags']:
            new_item = {}
            new_item['add_tag'] = True
            new_item['tag_name'] = item
            new_data.append(new_item)

    elif item == "container_pin_settings":
        new_data = []
        for item in data['data']:
            new_item = item
            del item['id']
            new_data.append(new_item)
            
    return new_data

def get_login():
    print("Username: ", end="")
    username = input()
    password = getpass.getpass("Password: ")
    if not username:
        print("Must specify a username to authenticate to Phantom.")
        sys.exit(2)

    if not password:
        print("Must specify a password to authenticate to Phantom.")
        sys.exit(3)
    return username, password

def get_csrf(session, url):
    pass

def get_session():
    s = requests.session()
    url = "https://{}/login".format(sys.argv[2])

    try:
        response = s.get(
            url,
            verify=VERIFY_CERT
        )
    except:
        print("Problems connecting to {}".format(url))
        sys.exit(4)

    if response.status_code < 200 or response.status_code > 299:
        print("An unsuccessful status code of {0} was returned for {1}.".format(response.status_code, url))
        sys.exit(5)

    pattern = ".*\"csrfmiddlewaretoken\" value=\"(.*)\""
    csrftokens = re.findall(pattern, response.text)

    if csrftokens:
        csrftoken = csrftokens[0]

    data = {
            'csrfmiddlewaretoken': csrftoken,
            'username': USERNAME,
            'password': PASSWORD
            }

    headers = {
            'Referer': url,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }

    try:
        response = s.post(
            url,
            verify=VERIFY_CERT,
            data=data,
            headers=headers
        )
    except:
        print("Problems connecting to {}".format(url))
        sys.exit(4)

    if response.status_code < 200 or response.status_code > 299:
        print("An unsuccessful status code of {0} was returned for {1}.".format(response.status_code, url))
        sys.exit(5)

    return s 


def make_rest_call(url, data, method="get", session=False):
    headers = {}
    cookies = {}

    if session:
        s = get_session()
        headers['Referer'] = url
    else:
        s = requests

    filepath = None
    if method != "post":
        filepath = data
        data = None

    try:
        request_func = getattr(s, method)
    except AttributeError:
        print('{0} attribute not found'.format(method))
        return None

    try:
        response = request_func(
            url,
            verify=VERIFY_CERT,
            auth=(USERNAME, PASSWORD),
            data=json.dumps(data),
            headers=headers
        )
    except Exception as e:
        print("Problems connecting to {}".format(url))
        print("Exception: {}".format(e))
        sys.exit(4)

    if response.status_code < 200 or response.status_code > 299:
        print("An unsuccessful status code of {0} was returned for {1}.".format(response.status_code, url))
        print(response.content)
        return None
    
    if filepath:
        try:
            file_content = response.json()
        except:
            print("Invalid JSON was returned from {}".format(url))
            print(response.headers)
            print(response.content)
            sys.exit(6)

        with open(filepath, "w") as f:
            json.dump(file_content, f)

def get_config():
    for item, value in ITEMS.items():
        if value is False:
            continue 

        if item == "system_settings":
            for inner_item, inner_value in value.items():
                if inner_value is False:
                    continue 
                print(inner_item, inner_value)
                url = BASE_URL + "/" + item + '?sections=["' + inner_item + '"]'
                filepath = OUTPUT_DIR + "/" + item + "_" + inner_item + ".json"
                make_rest_call(url, filepath)
        elif item in ["tags", "labels"]:
            print(item, value)
            url = BASE_URL + "/container_options"
            filepath = OUTPUT_DIR + "/" + item + ".json"
            make_rest_call(url, filepath)
        elif item in ["custom_fields"]:
            print(item, value)
            url = "https://{}/custom_container_fields/".format(sys.argv[2])
            filepath = OUTPUT_DIR + "/" + item + ".json"
            make_rest_call(url, filepath, "get", True)
        else:
            print(item, value)
            url = BASE_URL + "/" + item + "?page_size=0"
            filepath = OUTPUT_DIR + "/" + item + ".json"
            make_rest_call(url, filepath)
    return

def put_config():
    for item, value in ITEMS.items():
        if value is False:
            continue

        if item == "system_settings":
            for inner_item, inner_value in value.items():
                if inner_value is False:
                    continue 
                print(inner_item, inner_value)
                with open(OUTPUT_DIR + "/system_settings_" + inner_item + ".json", "r") as f:
                    post_body = clean_json(item, json.loads(f.read()))
                url = BASE_URL + "/" + item
                if inner_item not in ["audit_trail_settings", "auth_settings"]:
                    url = "{}/features".format(url)
                make_rest_call(url, post_body, "post")
        elif item == "labels":
            print(item, value)
            with open(OUTPUT_DIR + "/" + item + ".json", "r") as f:
                post_bodies = clean_json(item, json.loads(f.read()))
            url = BASE_URL + "/system_settings/events/"
            for post_body in post_bodies:
                make_rest_call(url, post_body, "post")
        elif item == "tags":
            print(item, value)
            with open(OUTPUT_DIR + "/" + item + ".json", "r") as f:
                post_bodies = clean_json(item, json.loads(f.read()))
            url = "https://{}/admin/admin_settings/tags/".format(sys.argv[2])
            print("Tags need to be added by hand.")
            print(post_bodies)
            # for post_body in post_bodies:
            #     make_rest_call(url, post_body, "post", True)
        elif item == "custom_fields":
            print(item, value)
            with open(OUTPUT_DIR + "/" + item + ".json", "r") as f:
                post_body = clean_json(item, json.loads(f.read()))
            url = BASE_URL + "/system_settings/events/".format(sys.argv[2])
            make_rest_call(url, post_body, "post")
        else:
            print(item, value)
            url = BASE_URL + "/" + item
            with open(OUTPUT_DIR + "/" + item + ".json", "r") as f:
                post_bodies = clean_json(item, json.loads(f.read()))
            for post_body in post_bodies:
                make_rest_call(url, post_body, "post")
    return


def get_usage():
    usage = "Usage: Specify an action (get or put) and the IP or hostname of the Phantom instance." \
            "\npython3 {0} get 192.168.1.42".format(sys.argv[0])
    return usage


if __name__ == "__main__":
    import sys
    import os
    import getpass
    import json
    import requests
    import re

    if VERIFY_CERT is False:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) < 3:
        print(get_usage())
        sys.exit(1)

    try:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
    except:
        print("Error creating output directory: {}".format(OUTPUT_DIR))
        sys.exit(7)

    BASE_URL = "https://{}/rest".format(sys.argv[2])
    USERNAME, PASSWORD = get_login()

    if sys.argv[1] == "get":
        get_config()
    elif sys.argv[1] == "put":
        put_config()
