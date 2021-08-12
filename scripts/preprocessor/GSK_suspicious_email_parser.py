from bs4 import UnicodeDammit
import traceback
import urllib
import urlparse
#
# Handle Domain Artitacts:
# 1. Remove "www.virustotal.com"
# 2. Remove "gsk.com" or "GSK.COM"
# 3. Remove "urldefense.com"
#
# Handle URL Artifacts:
# 1. Remove URLs containing "https://virustotal.com/en/search/query=*"
# 2. Remove "#" Value
# 3. Remove urldefense prefix from URLs
#

# return False to filter the artifact out of the list
def exclude_urls(artifact):

    supressed_urls = ['#']

    if artifact['name'] == 'URL Artifact':
        if artifact['cef'].get('requestURL', '') in supressed_urls:
            return False
        if 'www.virustotal.com' in artifact['cef'].get('requestURL', ''):
            return False
    return True

# return False to filter the artifact out of the list
def exclude_domains(artifact):

    supressed_domains = ['www.virustotal.com', 'gsk.com', 'GSK.COM', 'urldefense.com', 'www.microsoft.com', 
    'support.office.com', 'admin.microsoft.com', 'forms.office.com', 'go.microsoft.com', 'click.email.office.com',
    'view.email.office.com', 'image.email.office.com', 'www.office.com', 'techcommunity.microsoft.com',
    'docs.microsoft.com', 'cloudblogs.microsoft.com']

    if artifact['name'] == 'Domain Artifact':
        if artifact['cef'].get('destinationDnsDomain', '') in supressed_domains:
            return False
    return True

def decode_urls(artifacts):

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

            if urldefense in artifact['cef']['requestURL']:
                split_url = artifact['cef']['requestURL'].split(urldefense)[1]
                encoded = split_url.replace("*", "%")
                decoded = urllib.unquote(encoded)
                parsed_uri = urlparse(decoded)
                result = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri).replace('__', '')
                artifact['cef']['requestURL'] = result

        return artifacts[:]

# This is the official entry point tha the EWS App will call for each container.
def preprocess_container(container):

    artifacts = container.get('artifacts', [])

    if not len(artifacts):
        container['artifacts'] = []

    # Filter excluded URL Artifacts
    artifacts = filter(exclude_urls, artifacts)

    # Filter excluded Domain Artifacts
    artifacts = filter(exclude_domains, artifacts)

    # Decode requestURLs containing urldefense or safelinks
    # artifacts = decode_urls(artifacts)

    # Add list of Artifacts to 'artifacts' list of dicts
    container['artifacts'] = artifacts

    return container
