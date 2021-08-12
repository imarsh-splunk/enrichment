import urlparse


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

    # Decode requestURLs containing urldefense or safelinks
    artifacts = decode_urls(artifacts)

    # Add list of Artifacts to 'artifacts' list of dicts
    container['artifacts'] = artifacts

    return container