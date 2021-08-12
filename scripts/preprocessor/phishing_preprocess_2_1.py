#! /usr/bin/env python2
from __future__ import print_function

####################################################################################################

global args_debug
global args_strip_artifacts
global args_exclude_artifacts
global args_exclude_invalid_artifacts
global args_exclude_whitelisted_artifacts
global args_set_source_data_identifier

args_debug = False
args_strip_artifacts = False
args_exclude_artifacts = False
args_exclude_invalid_artifacts = False
args_exclude_whitelisted_artifacts = False
args_set_source_data_identifier = False

####################################################################################################

whitelist_domains = ["gsk.com", "office.com", "microsoft.com", "gmail.com"]
whitelist_url_hosts = ["www.virustotal.com"]
whitelist_url_domains = whitelist_domains + ["virustotal.com"]

####################################################################################################

"""
-----
https://help.proofpoint.com/Threat_Insight_Dashboard/Concepts/How_do_I_decode_a_rewritten_URL%3F
-----
As part of providing click-time protection, Proofpoint URL Defense messages'
links to point to the URL Defense Redirector service. Rewritten URLs are 
specially encoded to survive forwarding and other maniplations. This does mean 
that the embedded URL within the rewritten URL isn't completely transparent.
-----
a small Python utility which can be run on the command line:
-----
https://files.mtstatic.com/site_6638/177/1?Expires=1587067608&Signature=H8OdfhvOtkiHzMJ6RzRITvCrQgQTBsxcu8DUMy1w0j2vT2gAqti3FHcmLVUj3ttxxSS5eIQJ5MFti~SMlCa~t~HokE46CPyV13BAmntjiDzUVD5xNQC~~~LDYNJslXg8J3FSr2IEXQ5xCRcAF1UAcB~yIJ~jXwkPtaHd-X9UkiM_&Key-Pair-Id=APKAJ5Y6AV4GI7A555NA
-----
"""


import sys
import re
import string
from argparse import ArgumentParser
from base64 import urlsafe_b64decode
if sys.version_info[0] < 3:
    from urllib import unquote
    import HTMLParser
    htmlparser = HTMLParser.HTMLParser()
    unescape = htmlparser.unescape
    from string import maketrans
else:
    from urllib.parse import unquote
    from html import unescape
    maketrans = str.maketrans


class URLDefenseDecoder(object):

    @staticmethod
    def __init__():
        URLDefenseDecoder.ud_pattern = re.compile(r'https://urldefense(?:\.proofpoint)?\.com/(v[0-9])/')
        URLDefenseDecoder.v1_pattern = re.compile(r'u=(?P<url>.+?)&k=')
        URLDefenseDecoder.v2_pattern = re.compile(r'u=(?P<url>.+?)&[dc]=')
        URLDefenseDecoder.v3_pattern = re.compile(r'v3/__(?P<url>.+?)__;(?P<enc_bytes>.*?)!')
        URLDefenseDecoder.v3_token_pattern = re.compile("\*(\*.)?")
        URLDefenseDecoder.v3_run_mapping = {}
        run_values = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-' + '_'
        run_length = 2
        for value in run_values:
            URLDefenseDecoder.v3_run_mapping[value] = run_length
            run_length += 1

    def decode(self, rewritten_url):
        match = self.ud_pattern.search(rewritten_url)
        if match:
            if match.group(1) == 'v1':
                return self.decode_v1(rewritten_url)
            elif match.group(1) == 'v2':
                return self.decode_v2(rewritten_url)
            elif match.group(1) == 'v3':
                return self.decode_v3(rewritten_url)
            else:
                raise ValueError('Unrecognized version in: ', rewritten_url)
        else:
            raise ValueError('Does not appear to be a URL Defense URL')

    def decode_v1(self, rewritten_url):
        match = self.v1_pattern.search(rewritten_url)
        if match:
            url_encoded_url = match.group('url')
            html_encoded_url = unquote(url_encoded_url)
            url = unescape(html_encoded_url)
            return url
        else:
            raise ValueError('Error parsing URL')

    def decode_v2(self, rewritten_url):
        match = self.v2_pattern.search(rewritten_url)
        if match:
            special_encoded_url = match.group('url')
            trans = maketrans('-_', '%/')
            url_encoded_url = special_encoded_url.translate(trans)
            html_encoded_url = unquote(url_encoded_url)
            url = unescape(html_encoded_url)
            return url
        else:
            raise ValueError('Error parsing URL')

    def decode_v3(self, rewritten_url):
        def replace_token(token):
            if token == '*':
                character = self.dec_bytes[self.current_marker]
                self.current_marker += 1
                return character
            if token.startswith('**'):
                run_length = self.v3_run_mapping[token[-1]]
                run = self.dec_bytes[self.current_marker:run_length]
                self.current_marker += 1
                return run

        def substitute_tokens(text, start_pos=0):
            match = self.v3_token_pattern.search(text, start_pos)
            if match:
                start = text[start_pos:match.start()]
                built_string = start
                token = text[match.start():match.end()]
                built_string += replace_token(token)
                built_string += substitute_tokens(text, match.end())
                return built_string
            else:
                return text[start_pos:len(text)]

        match = self.v3_pattern.search(rewritten_url)
        if match:
            url = match.group('url')
            encoded_url = unquote(url)
            enc_bytes = match.group('enc_bytes')
            enc_bytes += '=='
            self.dec_bytes = (urlsafe_b64decode(enc_bytes)).decode('utf-8')
            self.current_marker = 0
            return substitute_tokens(encoded_url)

        else:
            raise ValueError('Error parsing URL')

urldefense_decoder = URLDefenseDecoder()

####################################################################################################

def strip_artifact(a):

    new_a = {}
    new_a['name'] = a['name']
    if args_set_source_data_identifier and 'source_data_identifier' in a:
        new_a['source_data_identifier'] = a['source_data_identifier']
    if 'cef' in a:
        new_a['cef'] = a['cef'].copy()
    return new_a

def strip_artifacts(artifacts):
    new_artifacts = []
    for a in artifacts:
        if 'cef' in a and 'original_artifact' in a['cef']:
            a['cef']['original_artifact'] = strip_artifact(a['cef']['original_artifact'])
        new_artifacts.append(strip_artifact(a))
    return new_artifacts

def exclude_artifacts(artifacts):
    new_artifacts = []
    for a in artifacts:
        name = a.get('name')
        if name not in ["Original Artifacts",
                "Invalid URL Artifact", "Invalid Domain Artifact",
                "Whitelisted URL Artifact", "Whitelisted Domain Artifact",
                "URL Artifact", "Domain Artifact"]:
            continue
        if args_exclude_invalid_artifacts:
            if name in ["Invalid URL Artifact", "Invalid Domain Artifact"]:
                continue
        if args_exclude_whitelisted_artifacts:
            if name in ["Whitelisted URL Artifact", "Whitelisted Domain Artifact"]:
                continue
        new_artifacts.append(a)
    return new_artifacts

def valid_url(url):
    if url.startswith("https://") or url.startswith("http://"):
        return True
    return False

import re

re_dns = re.compile(r"^([a-z0-9_-]+\.)+([a-z0-9_-]+)$", flags=re.IGNORECASE)

def valid_dns(domain):
    if re_dns.search(domain):
        return True
    return False
        
####################################################################################################

import urlparse

def whitelist_url_artifacts(artifacts):
    new_artifacts = []
    for a in artifacts:
        new_artifacts.append(a)
        if a.get('name') != "URL Artifact" or 'cef' not in a:
            continue

        url = a['cef'].get('requestURL')
        if not url:
            continue

        parsed = urlparse.urlsplit(url)
        host = parsed[1]
        # sanity check
        if not host:
            a['name'] = "Invalid URL Artifact"
            continue

        if host in whitelist_url_hosts:
            a['name'] = "Whitelisted URL Artifact"
            continue

        for candidate in whitelist_url_domains:
            if host.endswith(".{}".format(candidate)):
                a['name'] = "Whitelisted URL Artifact"
                break

    return new_artifacts

def whitelist_domain_artifacts(artifacts):
    new_artifacts = []
    for a in artifacts:
        new_artifacts.append(a)
        if a.get('name') and a['name'] != "Domain Artifact" or 'cef' not in a:
            continue

        domain = a['cef'].get('destinationDnsDomain')
        # sanity check
        if not domain:
            a['name'] = "Invalid Domain Artifact"
            continue

        if domain in whitelist_domains:
            a['name'] = "Whitelisted Domain Artifact"
            continue
        
        for candidate in whitelist_domains:
            if domain.endswith(".{}".format(candidate)):
                a['name'] = "Whitelisted Domain Artifact"
                break

    return new_artifacts

def exclude_whitelisted_artifacts(artifacts):
    new_artifacts = []
    for a in artifacts:
        if a.get('name') and a['name'].startswith("Whitelisted"):
            continue
        new_artifacts.append(a)
    return new_artifacts

####################################################################################################

def set_container_source_data_identifier(artifacts, sdi):
    for a in artifacts:
        a['source_data_identifier'] = sdi
    return artifacts

####################################################################################################

import urlparse, urllib, re

safelink = ".safelinks.protection.outlook.com"
urldefense = "urldefense.com"
virustotal = "https://www.virustotal.com/en/search?query="
re_safelink = re.compile(r"https*:/[^/][\w\.]+" + safelink.replace(".", r"\."))

def handle_decode(requesturl):
    if re_safelink.match(requesturl):
        requesturl = requesturl.replace("/", "//", 1)

    parsed = urlparse.urlsplit(requesturl)
    host = parsed[1]
    path = parsed[2]
    query = parsed[3]
    url = None
    if host.endswith(safelink):
        if query.startswith("url="):
            url = query.replace("url=", "", 1)

    elif host == urldefense:
        url = urldefense_decoder.decode(requesturl.encode('utf8'))

    elif requesturl.startswith(virustotal):
        url = requesturl.replace(virustotal, "")

    else:
        url = requesturl

    if url:
        url = urllib.unquote(url)
        if url != requesturl:
            return url

    return None

def process_requesturl(requesturl):
    lastret = requesturl
    nexturl = requesturl
    while True:
        ret = handle_decode(nexturl)
        if not ret:
            return lastret
        lastret = ret
        nexturl = ret

####################################################################################################

def preprocess_container(container):

    artifacts = container.get('artifacts')
    if not isinstance(artifacts, list):
        return container

    if args_debug:
        # save the original list of artifacts
        orig_artifacts = artifacts

        # apply debug changes to original list for clarity
        if args_exclude_artifacts:
            orig_artifacts = exclude_artifacts(orig_artifacts)

        if args_strip_artifacts:
            orig_artifacts = strip_artifacts(orig_artifacts)

        new_artifacts = [{
            'name': 'Original Artifacts',
            'cef': {
                'original_artifacts': orig_artifacts,
            }
        }]
    
    else:
        new_artifacts = []

    for a in artifacts:
        new_a = a.copy()
        if 'cef' in a:
            new_a['cef'] = a['cef'].copy()
        new_artifacts.append(new_a)
        if args_debug:
            if not 'cef' in new_a:
                new_a['cef'] = {}
            new_a['cef']['updated'] = False

        if new_a.get('name') and new_a['name'] == "URL Artifact":
            if 'cef' in new_a and 'requestURL' in new_a['cef']:
                url = new_a['cef']['requestURL']
                if not valid_url(url):
                    new_a['name'] = "Invalid URL Artifact"
                    if args_debug:
                        new_a['cef']['requestURL_valid'] = False
                    continue

                newurl = process_requesturl(url)

                if newurl.startswith("domain:"):
                    domain = newurl.replace("domain:", "", 1)
                    new_a['cef'] = {'destinationDnsDomain': domain}
                    new_a['name'] = "Domain Artifact"

                else:
                    new_a['cef']['requestURL'] = newurl
                    if not valid_url(newurl):
                        new_a['name'] = "Invalid URL Artifact"

                if args_debug:
                    new_a['cef'].update({
                        'original_artifact': a,
                        #'original_requestURL': a['cef']['requestURL'],
                        'requestURL_changed': True if new_a['cef'].get('requestURL') != a['cef']['requestURL'] else False,
                        'requestURL_valid': False if new_a['name'].startswith("Invalid") else True,
                        'updated': True,
                    })

        if new_a.get('name') and new_a['name'] == "Domain Artifact":
            if 'cef' in new_a and 'destinationDnsDomain' in new_a['cef']:
                domain = new_a['cef']['destinationDnsDomain']

                if domain.startswith("domain:"):
                    domain = domain.replace("domain:",1)
                    new_a['cef']['destinationDnsDomain'] = domain
                    if args_debug:
                        new_a['cef']['updated'] = True,

                if not valid_dns(domain):
                    new_a['name'] = "Invalid Domain Artifact"

                if args_debug:
                    new_a['cef']['destinationDnsDomain_valid'] = False if new_a['name'].startswith("Invalid") else True

    new_artifacts = whitelist_domain_artifacts(new_artifacts)
    new_artifacts = whitelist_url_artifacts(new_artifacts)

    if args_set_source_data_identifier:
        new_artifacts = set_container_source_data_identifier(new_artifacts, container['source_data_identifier'])

    if args_exclude_artifacts:
        new_artifacts = exclude_artifacts(new_artifacts)

    if args_exclude_whitelisted_artifacts:
        new_artifacts = exclude_whitelisted_artifacts(new_artifacts)

    if args_strip_artifacts:
        new_artifacts = strip_artifacts(new_artifacts)

    container['artifacts'] = new_artifacts
    return container

####################################################################################################

if __name__ == "__main__":
    import sys,os,json
    import argparse

    def whole_file(filename):
        with open(filename) as f:
            return f.read()

    # --- options parsing and management
    parser = argparse.ArgumentParser(description='preprocess container artifacts')
    parser.add_argument('container', nargs=1, metavar='container', help='container as json string in file')
    parser.add_argument('-d', '--debug', action='store_true', help='enable verbose debug code')
    parser.add_argument('-j', '--just-artifacts', action='store_true', help='output just the artifacts')
    parser.add_argument('-s', '--strip-artifacts', action='store_true', help='strip out everything except for the name and the cef fields')
    parser.add_argument('-x', '--exclude-artifacts', action='store_true', help='exclude everything except for URL and Domain artifacts')
    parser.add_argument('-i', '--exclude-invalid-artifacts', action='store_true', help='exclude "Invalid" artifacts')
    parser.add_argument('-w', '--exclude_whitelisted_artifacts', action='store_true', help='exclude "Whitelisted" artifacts')
    parser.add_argument('-r', '--set-source-data-identifier', action='store_true', help='set all artifacts source data identifier to be same as container')
    args = parser.parse_args()
    args_debug = args.debug
    args_strip_artifacts = args.strip_artifacts
    args_exclude_artifacts = args.exclude_artifacts
    args_exclude_invalid_artifacts = args.exclude_invalid_artifacts
    args_set_source_data_identifier = args.set_source_data_identifier
    args_exclude_whitelisted_artifacts = args.exclude_whitelisted_artifacts

    if not os.path.isfile(args.container[0]):
        print("Error: not a file; {}".format(args.container[0]), file=sys.stderr)
        exit(1)

    data = whole_file(args.container[0])
    obj = json.loads(data)

    if isinstance(obj, list):
        print("Loaded a list from file, taking first element", file=sys.stderr)
        obj = obj[0]

    if not isinstance(obj, dict):
        print("Error: unable to load a dict from file", file=sys.stderr)
        exit(2)

    print("Loaded a dict from file", file=sys.stderr)

    if not obj.get('container'):
        print("Error: did not find the container dict in json object", file=sys.stderr)
        exit(3)

    print("Found the container dict", file=sys.stderr)

    if obj.get('artifacts'):
        print("Found the adjacent artifacts dict", file=sys.stderr)
        container = obj['container'].copy()
        container['artifacts'] = obj.get('artifacts')
        container = preprocess_container(container)
        obj['artifacts'] = container['artifacts']

    elif obj['container'].get('artifacts'):
        print("Found the embeded artifacts dict", file=sys.stderr)
        container = preprocess_container(obj['container'])
        obj['container'] = container

    else:
        print("Error: did not find artifact dict in container dict", file=sys.stderr)
        exit(4)

    if args.just_artifacts:
        print(json.dumps(container['artifacts'], indent=4, sort_keys=True))
        
    else:
        print(json.dumps(obj, indent=4, sort_keys=True))
