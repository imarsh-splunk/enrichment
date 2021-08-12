import requests
from urlparse import urlparse
import urllib


def decode_urls(artifacts):

    artifacts_out = []
    for artifact in artifacts:

        urldefense = 'https://urldefense.com/v3/__'
        safelinks = 'safelinks.protection.outlook.com/?url='

        if artifact['name'] == 'URL Artifact':

            if safelinks in artifact['cef']['requestURL']:
                dest_url = artifact['cef']['requestURL'].split(safelinks)[1]
                encoded = dest_url.replace("*", "%")
                decoded = urllib.unquote(encoded)
                parsed_uri = urlparse(decoded)
                result = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri).replace('__', '')
                artifact['cef']['requestURL'] = result
                artifacts_out.append(artifact)

            if urldefense in artifact['cef']['requestURL']:
                split_url = artifact['cef']['requestURL'].split(urldefense)[1]
                encoded = split_url.replace("*", "%")
                decoded = urllib.unquote(encoded)
                parsed_url = urlparse(decoded)
                result = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_url).replace('__', '')
                artifact['cef']['requestURL'] = decoded
                artifacts_out.append(artifact)

        artifacts_out.append(artifact)

    artifacts_out = {v['id']: v for v in artifacts}.values()
    return artifacts_out


host = '172.16.133.128'
token = 'NvXVC0SV9jJvGDXgUw9Cy0YMRTrhWXQoQm7UnKZ5zX0='
headers = {"ph-auth-token": token}
# disable certificate warnings for self signed certificates
requests.packages.urllib3.disable_warnings()

container_id = 1100

r = requests.get('https://{}/rest/artifact?_filter_container_id={}&page_size=0'
                 .format(host, container_id), headers=headers, verify=False).json()['data']

output = decode_urls(r)
# print(output)

for i in output:
    print(i)
