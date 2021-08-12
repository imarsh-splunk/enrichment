from __future__ import print_function

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

# return False to filter the artifact out of the list
def exclude_urls(artifact):

    supressed_hosts = ['#', 'www.virustotal.com']
    supressed_hosts = ['#']

    if artifact.get('name') == 'URL Artifact':
        parsed = urlparse.urlsplit(artifact['cef'].get('requestURL', ''))
        host = parsed[1]

        if host in supressed_hosts:
            return False

    return True

# return False to filter the artifact out of the list
def exclude_domains(artifact):

    supressed_domains = ['www.virustotal.com', 'gsk.com', 'GSK.COM', 'urldefense.com', 'www.microsoft.com',
    'support.office.com', 'admin.microsoft.com', 'forms.office.com', 'go.microsoft.com', 'click.email.office.com',
    'view.email.office.com', 'image.email.office.com', 'www.office.com', 'techcommunity.microsoft.com',
    'docs.microsoft.com', 'cloudblogs.microsoft.com']

    if artifact.get('name') == 'Domain Artifact':
        if artifact['cef'].get('destinationDnsDomain', '') in supressed_domains:
            return False
    return True


####################################################################################################

import urlparse, urllib, re



safelink = ".safelinks.protection.outlook.com"
urldefense = "urldefense.com"
virustotal = "https://www.virustotal.com/en/search?query="
re_safelink = re.compile(r"https*:/[^/][\w\.]+" + safelink.replace(".", r"\."))

def _handle_decode(requesturl):
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

def _handle_requesturl(requesturl):
    lastret = None
    nexturl = requesturl
    while True:
        ret = _handle_decode(nexturl)
        if not ret:
            return lastret
        lastret = ret
        nexturl = ret

####################################################################################################

def preprocess_container(container):

    artifacts = container.get('artifacts', [])
    if not isinstance(artifacts, list):
        return container

    # Filter excluded URL Artifacts
    artifacts = filter(exclude_urls, artifacts)

    # Filter excluded Domain Artifacts
    artifacts = filter(exclude_domains, artifacts)

    if not artifacts:
        container['artifacts'] = []
        return container

    # saves the original container
    #new_artifacts = [{
    #    'name': 'Original JSON',
    #    'source_data_identifier': container.get('source_data_identifier'),
    #    'cef': {
    #        'json': json.dumps(container),
    #    }
    #}]
    new_artifacts = []

    container_sdi = container.get('source_data_identifier')
    for artifact in artifacts:
        requesturl = artifact.get('cef', {}).get('requestURL')
        if requesturl:
            newurl = _handle_requesturl(requesturl)
            if newurl:
                if newurl.startswith("domain:"):
                    domain = newurl.replace("domain:", "", 1)
                    artifact = {'name': 'Domain Artifact', 'cef':{'destinationDomain': domain}}

                else:
                    #artifact['cef']['original_link'] = artifact['cef']['requestURL']
                    artifact['cef']['requestURL'] = newurl
            
                if container_sdi:
                    artifact['source_data_identifier'] = container_sdi
                new_artifacts.append(artifact)

    # Filter excluded URL Artifacts
    new_artifacts = filter(exclude_urls, new_artifacts)

    # Filter excluded Domain Artifacts
    new_artifacts = filter(exclude_domains, new_artifacts)

    container['artifacts'] = new_artifacts
    return container

####################################################################################################

if __name__ == "__main__":
    import sys,os,json

    def whole_file(filename):
        with open(filename) as f:
            return f.read()

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        data = whole_file(sys.argv[1])
        obj = json.loads(data)

        if isinstance(obj, list):
            print("Loaded a list, taking first element", file=sys.stderr)
            obj = obj[0]

        print("Loaded a dict", file=sys.stderr)
        if isinstance(obj, dict):
            if obj.get('container'):
                print("Found the container dict", file=sys.stderr)
                if obj.get('artifacts'):
                    print("Found the adjacent artifacts dict", file=sys.stderr)
                    new_container = preprocess_container({'artifacts': obj.get('artifacts')})
                    obj['artifacts'] = new_container['artifacts']
                    print(json.dumps(obj, indent=4))
                    exit(0)

                elif obj['container'].get('artifacts'):
                    print("Found the embeded artifacts dict", file=sys.stderr)
                    obj['container'] = preprocess_container(obj['container'])
                    print(json.dumps(obj, indent=4))
                    exit(0)

    print("Didnt find the container dict", file=sys.stderr)
